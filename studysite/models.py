from operator import truediv
from xml.etree.ElementTree import tostring
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

# If the User model is constomized we need to change how we set up User
    #from django.contrib.auth import get_user_model
    #User = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField()

    def __str__(self):
        return self.user.username +  'Profile'

# class Course(models.Model):
#     course_name = models.CharField(max_length = 200, unique = True) # course long name i.e Partial Differential Equations
#     course_subject = models.CharField(max_length=5) # subject short hand i.e APMA
#     course_number = models.IntegerField(validators=MinValueValidator(0)) # course level i.e 3140
#     course_id = course_subject + " " + tostring(course_number) # course short hand name i.e APMA 3140
#     course_roster = models.ManyToManyField(User)
#
#        # self expressed as short hand and name i.e APMA 3140: Partial Differential Equations
#     def __str__(self):
#         return self.course_id+ ": " + self.course_name
