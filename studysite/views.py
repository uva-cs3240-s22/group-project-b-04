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

class UsersView(generic.ListView):
    model = User
    template_name = 'studysite/users.html'
    context_object_name = 'user_list'

    # def get_context_data(self, **kwargs):
    #     context = super(UsersView, self).get_context_data(**kwargs)
    #     context['object_list'] = UserProfile.objects.all()
    #     return context
    
    def get_queryset(self):
        return UserProfile.objects.all()
    
    # def addCourseToUser(request, self.pk, self):
    #     print("test")
    #     print(self)
    #     print(User.first_name)
    #     # Course.objects.get(pk=self.pk).course_roster.add(User)
    #     # User.objects.get(pk=User.pk).course_set.add(self)
    #     # return HttpResponseRedirect(reverse('course-finder'))


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