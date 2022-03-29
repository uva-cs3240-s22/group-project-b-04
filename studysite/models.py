from operator import truediv
from xml.etree.ElementTree import tostring
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

# If the User model is constomized we need to change how we set up User
from django.contrib.auth import get_user_model
class Course(models.Model):
    course_name = models.CharField(max_length = 200, unique = True) # course long name i.e Partial Differential Equations
    course_subject = models.CharField(max_length=5) # subject short hand i.e APMA
    course_number = models.CharField(max_length=5) # course level i.e 3140
    User = get_user_model()
    course_roster = models.ManyToManyField(User)

    # self expressed as short hand and name i.e APMA 3140: Partial Differential Equations
    def __str__(self):
        return self.course_name

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses_enrolled = models.ManyToManyField(Course)

    def __str__(self):
        return f'{self.user.username} Profile'

#create another model, call it profile manager, creating a profile model that includes the user and all the other parameters i want