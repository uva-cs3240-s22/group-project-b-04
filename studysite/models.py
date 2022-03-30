from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

years = (('Undergraduate', 'Undergraduate'), ('Masters', 'Masters'), ('PhD', 'PhD'))

# If the User model is constomized we need to change how we set up User
from django.contrib.auth import get_user_model
class Course(models.Model):
    course_name = models.CharField(max_length = 200, unique = True) # course long name i.e Partial Differential Equations
    course_subject = models.CharField(max_length=5) # subject short hand i.e APMA
    course_number = models.CharField(max_length=5) # course level i.e 3140
    course_roster = models.ManyToManyField(User, blank=True) # to access from user profile do the user.course_set.all()

    # self expressed as short hand and name i.e APMA 3140: Partial Differential Equations
    def __str__(self):
        return self.course_name
      
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=True, blank=True)
    major = models.CharField(max_length=80, blank=True)
    year = models.CharField(max_length=80, choices=years, blank=True)
    bio = models.TextField(max_length=250, default='', blank=True)
    # courses_list = models.ManyToManyField(Course, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('profile saved')
    instance.userprofile.save()