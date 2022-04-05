from multiprocessing import context
from re import template
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

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


class CoursesView(generic.ListView):
    model = Course
    template_name = 'studysite/courses.html'
    context_object_name = 'courses_list'

    def get_queryset(self):
        return Course.objects.order_by('course_subject')
    
class BuddyView(generic.ListView):
    model=User
    template_name = 'studysite/restricted/buddy.html'

    context_object_name = "user_list"

    def get_queryset(self):
        return User.objects.all()

class NotifView(generic.ListView):
    model=FriendRequest
    template_name = "studysite/restricted/notifications.html"

    context_object_name = "request_list"

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

def addcourse(request):
    if request.method == "POST" :
        if (len(request.POST['course_subject']) > 0 and len(request.POST['course_name']) > 0 and len(request.POST['course_number']) > 0 ):
            course = Course(course_name = request.POST['course_name'], course_number = request.POST['course_number'], course_subject = request.POST['course_subject'])
            course.save()
            return HttpResponseRedirect(reverse('course-finder'))
        else: 
            return render(request, 'studysite/restricted/courseadd.html', {'error_message': "That class already exists or is incorrect",})
    else:
        return render(request, 'studysite/restricted/courseadd.html')

def addCourseToUser(request, pk, pku):
    course = get_object_or_404(Course, pk=pk)
    try:
        selected_course = Course.objects.get(pk=pk)
    except (KeyError, Course.DoesNotExist):
        # Redisplay the question voting form.
        print("Website doesn't exist")
        return render(request, 'studysite/courses.html', {
            'courses_list': Course.objects.order_by('course_subject'),
        })
    else:
        selected_course.course_roster.add(User.objects.get(pk=pku))
        #ProfileView.request.user.pk
        selected_course.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'studysite/courses.html', {
            'courses_list': Course.objects.order_by('course_subject'),
        })

def send_friend_request(request, uid):
    fromu = request.user
    tou = User.objects.get(id=uid)
    if  fromu not in tou.userprofile.friends.all():
        friend_request, created = FriendRequest.objects.get_or_create(from_user=fromu, to_user=tou)
        if created :
            return HttpResponse('friend request sent')
        else :
            return HttpResponse('you have already requested from this user')
    else :
        return HttpResponse('You are already friends with this user')

def accept_friend_request(request, rid):
    friend_request = FriendRequest.objects.get(id=rid)
    if friend_request.to_user == request.user:
        friend_request.to_user.userprofile.friends.add(friend_request.from_user)
        friend_request.from_user.userprofile.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else :
        return HttpResponse('friend request not accepted')