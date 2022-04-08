from django.contrib import admin
from .models import *


class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('course_roster',)

class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('friends',)

class EventAdmin(admin.ModelAdmin):
    filter_horizontal = ('event_list',)

# Register your models here.
admin.site.register(Course, CourseAdmin)
admin.site.register(UserProfile, UserProfileAdmin)