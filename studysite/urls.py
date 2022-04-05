"""studybuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from studysite import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view(), name='logout'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('<str:username>/profile', views.ProfileView.as_view(), name='profile'),
    path('courses/', views.CoursesView.as_view(), name='course-finder'),
    path('courses/add/', views.addcourse, name="course-add"),
    path('courses/<int:pk>/<int:pku>/', views.addCourseToUser, name='course-add-user'),
    path('send_friend_request/<int:uid>/', views.send_friend_request, name="send friend request"),
    path('accept_friend_request/<int:rid>/', views.accept_friend_request, name="accept friend request"),
    path('buddies/', views.BuddyView.as_view(), name='buddy-finder'),
    path('notifications/', views.NotifView.as_view(), name='notifications'),
]
