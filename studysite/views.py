from multiprocessing import Event, context
from re import template
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save
from django.shortcuts import redirect
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError, send_mail
import google_auth_oauthlib
from django.core.paginator import Paginator
from psycopg2 import Date
from .models import *
from datetime import date, time, datetime, timedelta
from django.urls import reverse_lazy
from .forms import UserProfileForm, ContactUsForm
import requests
import json
import re
from datetime import date, time, datetime, timedelta
from django.urls import reverse_lazy
from .forms import UserProfileForm
import requests
import json

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

import datefinder

FILTER_TYPES = {
    'SUBJECT'   :   'SUBJECT',
    'NUMBER'    :   'NUMBER',
    'NAME'  :   'NAME',
    'DATE'  :   'DATE',
    'FULL'  :   'FULL',
    'ALL'   :   'ALL',
}


# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'studysite/index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class AboutView(generic.TemplateView):
    template_name = 'studysite/about.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class ThanksView(generic.TemplateView):
    template_name = 'contactus_form/thanks.html'

    # def get_context_data(self, **kwargs):
    #     return super().get_context_data(**kwargs)
class StudySpacesView(generic.TemplateView):
    template_name = 'studysite/studySpaces.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class LoginView(generic.TemplateView):
    template_name = 'studysite/registration/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

#postprofile based on https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/#:~:text=instance.profile.save%20%28%29%20You%20can%20get%20confused%20from%20this,The%20other%20method%20save_profile%20just%20saves%20the%20instance.
def postprofile(request, username):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=(request.user.username,)))
       # return render(request, 'studysite/userprofile_form.html', {'form': form})
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'studysite/restricted/userprofile_form.html', {'form': form})

class ProfileView(LoginRequiredMixin, generic.DetailView):
    permission_denied_message = "Please login to view this page."
    model = User
    template_name = 'studysite/restricted/profile.html'
    context_object_name = 'courses_list'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context["friends"] = self.model.objects.get(pk=self.request.user.pk).userprofile.friends.all()
        context["courses"] = self.model.objects.get(pk=self.request.user.pk).course_set.all()
        return context
    
    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)

class DashView(LoginRequiredMixin, generic.DetailView):
    permission_denied_message = "Please login to view this page."
    model = User
    template_name = 'studysite/restricted/dashboard.html'
    
    def get_context_data(self, **kwargs):
        return {'event_list': self.model.objects.get(pk=self.request.user.pk).events.filter(time__gte = datetime.today())}

    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)


def showcourse():
    try:
        Course.objects.count()
    except (KeyError, Course.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
    else:
        url = 'https://api.devhub.virginia.edu/v1/courses'
        data = requests.get(url).json()
        class_list = []
        if Course.objects.count() == 0:
            for item in data["class_schedules"]["records"]:
                classCourse = str(item[1]) + str(item[0])
                if classCourse not in class_list:
                    class_list.append(classCourse)
                    course = Course(course_number=item[1], course_subject=item[0], course_name=item[4])
                    course.save()

class CoursesView(LoginRequiredMixin, generic.ListView):
    permission_denied_message = "Please login to view this page."
    model = Course
    template_name = 'studysite/restricted/courses.html'
    context_object_name = 'courses_list'
    showcourse()
    paginate_by = 25

    def get_queryset(self):
        return get_filtered_courses(self.kwargs['filtered'])


class EventView(generic.ListView):
    model = StudyEvent
    template_name = 'studysite/restricted/studyeventlist.html'
    template_name = 'studysite/restricted/studyeventlist.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return self.model.objects.filter(time__gte = datetime.today())


class DetailEventView(generic.DetailView):
    model = StudyEvent
    template_name = 'studysite/restricted/studyevent.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = self.get_object().users.all
        return context
    


class BuddyView(LoginRequiredMixin, generic.ListView):
    permission_denied_message = "Please login to view this page."
    model=User
    template_name = 'studysite/restricted/buddy.html'

    context_object_name = "user_list"


    def get_queryset(self):
        return User.objects.all()

class MessageView(LoginRequiredMixin, generic.ListView):
    permission_denied_message = "Please login to view this page."
    model=User
    template_name = 'studysite/restricted/messages.html'

    context_object_name = "user_list"

    def get_queryset(self):
        return User.objects.all()

class NotifView(LoginRequiredMixin, generic.ListView):
    permission_denied_message = "Please login to view this page."
    model=FriendRequest
    template_name = "studysite/restricted/notifications.html"

    context_object_name = "request_list"

    def get_context_data(self, **kwargs):
        return {'request_list': FriendRequest.objects.filter(to_user=self.request.user), 'msg_list': Message.objects.filter(to_user=self.request.user)}

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)

# limit access to only logged in users, otherwise redirect to login page
def validate_user(request):
    if not request.user.is_authenticated:
        return render(request, reverse('login'), {
            'error_message': "Please login to view this page.",
        })
    else:
        return HttpResponseRedirect(reverse('profile'))

def to_time(time):
    first_two = time[0:2]
    to_int = int(first_two)
    sec_two = time[3:5]
    if (to_int < 12 ):
        time1 = str(to_int) + ':' + sec_two + 'AM'
        return time1
    elif(to_int == 12):
        time2 = str(to_int) + ':' + sec_two + 'PM'
        return time2
    else:
        actual = to_int - 12
        time3 = str(actual) + ':' + sec_two + 'PM'
        return time3

def addcourse(request):
    if request.method == "POST" :
        if (len(request.POST['course_subject']) > 0 and len(request.POST['course_name']) > 0 and len(request.POST['course_number']) > 0 ):
            if (Course.objects.filter(course_subject=request.POST['course_subject'].upper(), course_number=request.POST['course_number']).count() == 0):
                url = 'https://api.devhub.virginia.edu/v1/courses'
                data = requests.get(url).json()
                instructor = []
                class_instructor = ""
                #class_formal_descript = []
                course_subject = request.POST['course_subject']
                course_number = request.POST['course_number']
                for item in data["class_schedules"]["records"]:
                    if (item[0] == course_subject) and (item[1] == course_number):
                        if item[6] not in instructor:
                            if item[6] != "":
                                instructor.append(item[6])
                                class_instructor = item[6] + " " + item[8] + ": " + to_time(item[9]) + "-" + to_time(item[10]) + "\n" + class_instructor
                        #class_formal_descript = item[5]
                        #break
                course = Course(course_name = request.POST['course_name'], course_number = request.POST['course_number'], course_subject = request.POST['course_subject'].upper())
                course.class_instructor = class_instructor
                course.save()
                return addCourseToUser(request, course.pk, request.user.pk)
            else: 
                return render(request, 'studysite/restricted/courseadd.html', {'error_message': "That class already exists",})
        else: 
            return render(request, 'studysite/restricted/courseadd.html', {'error_message': "That input is incorrect",})
    else:
        return render(request, 'studysite/restricted/courseadd.html')

def addStudyEvent(request):
    if request.method == "POST" :
        owner = request.user
        date_obj = date.fromisoformat(request.POST['meeting_date'])
        time_obj = time.fromisoformat(request.POST['start_time'])
        date_time = datetime.combine(date_obj, time_obj)
        event = StudyEvent(owner = owner, course = Course.objects.get(id=int(request.POST['event_course'])), max_users = request.POST['max-users'], time = date_time, description = request.POST['description'])
        coursename = event.course.course_subject + " " + event.course.course_number
        email = request.user.email
        created_event = create_event(date_time, coursename, event.description, email)
        event.event_id = created_event['id']
        print("the event id")
        print(event.event_id)
        event.save()
        return addUserToEvent(request, event.pk, owner.pk)
    else:
            return render(request, 'studysite/restricted/addstudyevent.html', {
            'courses_list': Course.objects.order_by('course_subject'),})

#def deleteUserOrCourse(request, pk, pku):


#def deleteUserOrCourse(request, pk, pku):

def contactus(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            subject = "Study Buddy Question"
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            question = "First name: " + first_name + "\n" + "Last name: " + last_name + "\n" + "Email: " + email + "\n" + "Question: " + form.cleaned_data['question']
        try:
            send_mail(subject, question, 'megan2022stuff@gmail.com', ['megan2020stuff@gmail.com'])
        except BadHeaderError:
            return render(request, "studysite/contactus_form.html", {'form':form, 'error_message': "Invalid Header",})
        return render(request, "studysite/contactus_form.html", {'form': ContactUsForm(), 'error_message': "Thanks for the message! We'll Reach out to you soon!",})
    form = ContactUsForm()
    return render(request, "studysite/contactus_form.html", {'form':form, 'error_message': "",})

def addUserToEvent(request, pk, pku):
    course = get_object_or_404
    try:
        selected_event = StudyEvent.objects.get(pk=pk)
    except (KeyError, StudyEvent.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
        return HttpResponseRedirect(reverse('event-finder'))
    else:
        selected_event.users.add(User.objects.get(pk=pku))
        if User.objects.get(pk=pku).email != '':
            update_event(User.objects.get(pk=pku).email, selected_event.event_id)
        selected_event.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('event-finder'))

def deleteUserFromEvent(request, uid, pk):
    studyevent = get_object_or_404(StudyEvent, pk=pk)
    try:
        selected_event = StudyEvent.objects.get(pk=pk)
    except (KeyError, StudyEvent.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
        return HttpResponseRedirect(reverse('event-finder'))
    else:
        selected_event.users.remove(uid)
        if request.user.email != '':
            delete_event_fromUser(request.user.email, selected_event.event_id)
        # ProfileView.request.user.pk
        selected_event.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('event-finder'))

def addCourseToUser(request, pk, pku):
    course = get_object_or_404(Course, pk=pk)
    try:
        selected_course = Course.objects.get(pk=pk)
    except (KeyError, Course.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
        return HttpResponseRedirect(reverse('course-finder', kwargs={'filtered':'all',}))
    else:
        selected_course.course_roster.add(User.objects.get(pk=pku))
        #ProfileView.request.user.pk
        selected_course.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('course-finder', kwargs={'filtered':'all',}))

def deleteCourseFromUser(request, uid, pk):
    if 'delete_course' in request.POST :
        course = get_object_or_404(Course, pk=pk)
        try:
            selected_course = Course.objects.get(pk=pk)
        except (KeyError, User.DoesNotExist):
            # Redisplay the question voting form.
            print("Website doesn't exist")
            return HttpResponseRedirect(reverse('dashboard', kwargs={'username': User.objects.get(id=uid).username,}))
        else:
            selected_course.course_roster.remove(uid)
            selected_course.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('dashboard', kwargs={'username': User.objects.get(id=uid).username,}))
    else :
        return deleteUserFromEvent(request=request, uid=uid, pk=pk)

def send_friend_request(request, uid):
    fromu = request.user
    tou = User.objects.get(id=uid)
    if  fromu not in tou.userprofile.friends.all():
        # check not already a request from the tou
        try:
            friend_request = FriendRequest.objects.get(from_user=tou, to_user=fromu)
        except:
            friend_request, created = FriendRequest.objects.get_or_create(from_user=fromu, to_user=tou)
            if created :
                tou.userprofile.num_alerts = tou.userprofile.num_alerts + 1
                tou.save()
                return HttpResponseRedirect(reverse('buddy-finder', kwargs={'friend_message': "Friend Request Sent",}))#render(request, 'studysite/restricted/buddy.html', {'friend_message': "Friend Request Sent",})
            else :
                return HttpResponseRedirect(reverse('buddy-finder', kwargs={'friend_message': "You already have a pending request to this user",}))
        else:
            return HttpResponseRedirect(reverse('buddy-finder', kwargs={'friend_message': "You have a pending request from this user, check your notifications to accept",}))
    else :
        return HttpResponseRedirect(reverse('buddy-finder', kwargs={'friend_message': "You are already friends with this user!",}))

def accept_friend_request(request, rid):
    friend_request = FriendRequest.objects.get(id=rid)
    if request.POST['action'] == "Deny":
        friend_request.delete()
    elif friend_request.to_user == request.user:
        friend_request.to_user.userprofile.friends.add(friend_request.from_user)
        friend_request.from_user.userprofile.friends.add(friend_request.to_user)
        friend_request.delete()
    if request.user.userprofile.num_alerts > 0:
        request.user.userprofile.num_alerts = request.user.userprofile.num_alerts - 1
    request.user.save()
    return HttpResponseRedirect(reverse('notifications'))

def msgBuddy(request, uid):
    fromu = request.user
    tou = User.objects.get(id=uid)
    if request.method == "POST" :
        message = Message(from_user = fromu, to_user = tou, msg_content = request.POST['message'])
        tou.userprofile.num_alerts = tou.userprofile.num_alerts + 1
        tou.save()
        message.save()
    return render(request, 'studysite/restricted/messages.html', {
            'user_list': User.objects.all(),
        })

def deleteMsg(request, pk):
    message = get_object_or_404(Message, pk=pk)
    try:
        msg = Message.objects.get(pk=pk)
    except (KeyError, User.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
        return HttpResponseRedirect(reverse('notifications'))
    else:
        msg.delete()
        if request.user.userprofile.num_alerts > 0:
            request.user.userprofile.num_alerts = request.user.userprofile.num_alerts - 1
        request.user.save()
        return HttpResponseRedirect(reverse('notifications'))



# REFERENCE GOOGLE CALENDAR API INTEGRATION
# https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322
# Code Version: 2019
# Date Viewed: 4/11/22

scopes = ['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
#credentials = flow.run_console()
#pickle.dump(credentials, open("token.pkl", "wb"))
credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)
result = service.calendarList().list().execute()
calendar_id = 0
for entry in result['items']:
    if entry['summary'] == 'Study Buddy Events':
        calendar_id = entry['id']
        break

def create_event(start_time, summary, description, email, duration=1, location=None, ):
    end_time = start_time + timedelta(hours=duration)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'attendees' : [
            {'email': email },
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    event = service.events().insert(calendarId=calendar_id, body=event, sendUpdates='all').execute()
    print(event['id'])
    return event

def update_event(email, event_id):
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    email = {'email': email, 'responseStatus': 'accepted'}
    exists1 = False
    for index in range(len(event['attendees'])):
        if email == event['attendees'][index]:
            exists1 = True
    if exists1 == False :
        event['attendees'].append(email)
    print(event['attendees'])
    return service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()

def delete_event_fromUser(email, event_id):
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    email = {'email': email, 'responseStatus': 'accepted'}
    new_email_list = []
    for index in range(len(event['attendees'])):
        spec_email = event['attendees'][index]
        if email != spec_email:
            new_email_list.append(spec_email)
    email3 = {'email': 'megan2022stuff@gmail.com', 'responseStatus': 'needsAction'}
    new_email_list.append(email3)
    event['attendees'] = new_email_list
    return service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()

def course_search(request):
    if request.method == "POST":
        if (len(request.POST['searched'])<1):
            return HttpResponseRedirect(reverse('course-finder', kwargs={'filtered':'all'}))
        else:
            return HttpResponseRedirect(reverse('course-finder', kwargs={'filtered' : request.POST['searched']}))
    return HttpResponseRedirect(reverse('course-finder', kwargs={'filtered':'all'}))

def get_filtered_courses(term):
    searched = term.split()# list of search terms of searched terms w/out whitespace
    search_type = classify(searched[0])
    if search_type == FILTER_TYPES['SUBJECT']:
        subject = searched[0].upper()
        if len(searched) > 1:
            num = searched[1]
            if classify(num) == FILTER_TYPES['NUMBER']:
                #print(num)
                return Course.objects.filter(course_subject=subject, course_number = num)
        else:
            return Course.objects.filter(course_subject=subject)
    elif search_type == FILTER_TYPES['NAME']:
        return Course.objects.filter(course_name = term)
    else:
        return Course.objects.all() #order_by('course_subject')

def classify(term):
    subject = re.compile('[A-Z]{2,5}') # 2-5 characters of capital letters
    number = re.compile('[0-9]{4}') # 4 digits
    date = list(datefinder.find_dates(term, strict=False, base_date=datetime(2022,1,1)))
    if term.upper() == 'ALL':
        return FILTER_TYPES['ALL']
    if subject.search(term.upper()) != None and len(term) < 5:
        return FILTER_TYPES['SUBJECT']
    elif number.search(term) != None:
        return FILTER_TYPES['NUMBER']
    elif date:
        return FILTER_TYPES['DATE']
    elif term.lower() == "open" or term.lower() == 'available':
        return FILTER_TYPES['FULL']
    else:
        return FILTER_TYPES['NAME']


