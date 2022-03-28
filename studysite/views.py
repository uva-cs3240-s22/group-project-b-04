from re import template
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.views import generic
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class AboutView(generic.TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class LoginView(generic.TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class ProfileView(LoginRequiredMixin, generic.DetailView):
    permission_denied_message = "Please login to view this page."
    model = Profile
    template_name = 'restricted/profile.html'
    
    def get_object(self):
        return self.model.objects.get(pk=self.request.user.pk)


# limit access to only logged in users, otherwise redirect to login page
def validate_user(request, username, ):
    if not request.user.is_authenticated:
        return render(request, reverse('login'), {
            'error_message': "Please login to view this page.",
        })
    else:
        return HttpResponseRedirect(reverse('profile'))