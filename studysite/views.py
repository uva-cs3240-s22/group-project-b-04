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
import google_auth_oauthlib
from psycopg2 import Date
from .models import *
<<<<<<< HEAD
<<<<<<< HEAD
from datetime import date, time, datetime, timedelta
import re
=======
from .calendar_API import test_calendar
from datetime import date, time, datetime, timedelta
from django.urls import reverse_lazy
from .forms import UserProfileForm
import requests
import json

>>>>>>> 178fb8d (applied class api and created form to edit profile)

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
=======
from .calendar_API import test_calendar
>>>>>>> 888d472 (adding calendar changes)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'studysite/index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class AboutView(generic.TemplateView):
    template_name = 'studysite/about.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class LoginView(generic.TemplateView):
    template_name = 'studysite/registration/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

# class EditProfileView(LoginRequiredMixin, TemplateView):
#     permission_denied_message = "Please login to view this page."
#    # profile_form = UserProfileForm
    #model = UserProfile
   # template_name = 'studysite/userprofile_form.html'
   #  def post(request):
   #      if request.method == "POST" :
   #          year_obj = year.fromisoformat(request.POST['user_year'])
   #          major_obj = major.fromisoformat(request.POST['user_major'])
   #          bio_obj = bio.fromisoformat(request.POST['user_bio'])
   #          profile = UserProfile(year=year_obj, major=major_obj, bio=bio_obj)
   #          profile.save()
   #      return render(request, 'studysite/userprofile_form.html', UserProfile.objects.all())

    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)
    # def previous(request):
    #     return HttpResponseRedirect(reverse('profile'))

    #template_name = 'studysite/restricted/edit_profile.html'
    #success_url = reverse_lazy('profile user.username')

def post(request, username):
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
    return render(request, 'studysite/userprofile_form.html', {'form': form})
    # if request.method == "POST" :
    #     form = UserProfileForm(request.POST)
    #     if form.is_valid():
    #         profile = UserProfile(user=request.user, year=request.POST['user_year'], major=request.POST['user_major'], bio=request.POST['user_bio'])
    #         profile.save()
    # return render(request, 'studysite/userprofile_form.html')

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


class CoursesView(LoginRequiredMixin, generic.ListView):
    permission_denied_message = "Please login to view this page."
    model = Course
    template_name = 'studysite/restricted/courses.html'
    context_object_name = 'courses_list'

    def get_queryset(self):
        return get_filtered_courses(self.kwargs['filtered'])

class EventView(generic.ListView):
    model = StudyEvent
    template_name = 'studysite/restricted/studyeventlist.html'
    context_object_name = 'event_list'

    def get_queryset(self):
        return self.model.objects.filter(time__gte = datetime.today())
    

class BuddyView(LoginRequiredMixin, generic.ListView):
    permission_denied_message = "Please login to view this page."
    model=User
    template_name = 'studysite/restricted/buddy.html'

    context_object_name = "user_list"

    def check_pending(fromu, tou):
        return fromu.from_user.filter(to_user=tou)

    def get_queryset(self):
        return User.objects.all()

class MessageView(LoginRequiredMixin, generic.ListView):
    permission_denied_message = "Please login to view this page."
    model=User
    template_name = 'studysite/restricted/messages.html'

    context_object_name = "user_list"

    def check_pending(fromu, tou):
        return fromu.from_user.filter(to_user=tou)

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
                return HttpResponseRedirect(reverse('course-finder', kwargs={'filtered':'all',}))
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
        #print(type(time))
        time_obj = time.fromisoformat(request.POST['start_time'])
        #print(type(time_obj))
        #time_obj = time.strptime(request.POST['start_time'],"%H:%M")
        date_time = datetime.combine(date_obj, time_obj)
        #print(type(request.POST['event_course']))
        event = StudyEvent(owner = owner, course = Course.objects.get(id=int(request.POST['event_course'])), max_users = request.POST['max-users'], time = date_time, description = request.POST['description'])
        event.save()
        create_event(date_time, event.description)
    return render(request, 'studysite/restricted/addstudyevent.html', {
            'courses_list': Course.objects.order_by('course_subject'),
        })

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
        #ProfileView.request.user.pk
        selected_event.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('event-finder'))

def deleteUserFromEvent(request, uid, pk):
    return

def addCourseToUser(request, pk, pku):
    course = get_object_or_404(Course, pk=pk)
    try:
        selected_course = Course.objects.get(pk=pk)
    except (KeyError, Course.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
        return render(request, 'studysite/restricted/courses.html', {
            'courses_list': Course.objects.order_by('course_subject'),
        })
    else:
        selected_course.course_roster.add(User.objects.get(pk=pku))
        #ProfileView.request.user.pk
        selected_course.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'studysite/restricted/courses.html', {
            'courses_list': Course.objects.order_by('course_subject'),
        })
<<<<<<< HEAD

def deleteCourseFromUser(request, uid, pk):
    course = get_object_or_404(Course, pk=pk)
    try:
        selected_course = Course.objects.get(pk=pk)
    except (KeyError, User.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
        return HttpResponseRedirect(reverse('dashboard', kwargs={'username': User.objects.get(id=uid).username,}))
    else:
        selected_course.course_roster.remove(uid)
        print(selected_course.course_roster.all())
        #ProfileView.request.user.pk
        selected_course.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('dashboard', kwargs={'username': User.objects.get(id=uid).username,}))

def send_friend_request(request, uid):
    fromu = request.user
    tou = User.objects.get(id=uid)
    if  fromu not in tou.userprofile.friends.all():
        # check not already a request from the tou
        try:
            friend_request = FriendRequest.objects.get(from_user=tou, to_user=fromu)
            return HttpResponseRedirect(reverse('buddy-finder', kwargs={'friend_message': "You have a pending request from this user, check your notifications to accept",}))#render(request, 'studysite/restricted/buddy.html', {'friend_message': "You have a pending request from this user, check your notifications to accept",})
        except:
            friend_request, created = FriendRequest.objects.get_or_create(from_user=fromu, to_user=tou)
            if created :
                return HttpResponseRedirect(reverse('buddy-finder', kwargs={'friend_message': "Friend Request Sent",}))#render(request, 'studysite/restricted/buddy.html', {'friend_message': "Friend Request Sent",})
            else :
                return render(request, 'studysite/restricted/buddy.html', {'friend_message': "You already have a pending request to this user"})
    else :
        return render(request, 'studysite/restricted/buddy.html', {'friend_message': "You are already friends with this user",})

def accept_friend_request(request, rid):
    friend_request = FriendRequest.objects.get(id=rid)
    if friend_request.to_user == request.user:
        friend_request.to_user.userprofile.friends.add(friend_request.from_user)
        friend_request.from_user.userprofile.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponseRedirect(reverse('notifications'))
    else :
        return HttpResponseRedirect(reverse('notifications'))

def msgBuddy(request, uid):
    fromu = request.user
    tou = User.objects.get(id=uid)
    if request.method == "POST" :
        message = Message(from_user = fromu, to_user = tou, msg_content = request.POST['message'])
        message.save()
    return render(request, 'studysite/restricted/messages.html', {
            'user_list': User.objects.all(),
        })

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





def create_event(start_time, summary, duration=1, description=None, location=None):
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
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()

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

=======
def calendar(request):
    results = test_calendar()
    context = {"results": results}
    return render(request, 'studysite/calendar.html', context)
>>>>>>> 888d472 (adding calendar changes)
