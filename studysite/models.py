from email.policy import default
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save
<<<<<<< HEAD
from django.utils.timezone import now
=======
#from oauth2client.contrib.django_util.models import CredentialsField
>>>>>>> 6db00cf (add requirements.txt)

# Create your models here.

years = (('Undergraduate', 'Undergraduate'), ('Masters', 'Masters'), ('PhD', 'PhD'))

# If the User model is constomized we need to change how we set up User
    #from django.contrib.auth import get_user_model
    #User = get_user_model()
class Course(models.Model):
    course_name = models.CharField(max_length = 200) # course long name i.e Partial Differential Equations
    course_subject = models.CharField(max_length=5) # subject short hand i.e APMA
    course_number = models.CharField(max_length=5) # course level i.e 3140
    course_roster = models.ManyToManyField(User, blank=True) # to access from user profile do the user.course_set.all()
    class_instructor = models.CharField(max_length=15, blank=True, null=True)
    class_formal_descript = models.CharField(max_length=200, blank=True, null=True)
    # self expressed as short hand and name i.e APMA 3140: Partial Differential Equations
    def __str__(self):
        return f"{self.course_subject} {self.course_number}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, null=True, blank=True)
    major = models.CharField(max_length=80, blank=True)
    year = models.CharField(max_length=80, choices=years, blank=True)
    bio = models.TextField(max_length=250, default='', blank=True)
    friends = models.ManyToManyField(User, related_name="friends", blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile')

  #  def __str__(self):
     #   return f"{self.user.username}'s Profile"

<<<<<<< HEAD
class StudyEvent(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='%(class)s_requests_created')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
<<<<<<< HEAD
    users = models.ManyToManyField(User, related_name="events")
=======
    users = models.ManyToManyField(User, blank=True)
>>>>>>> 63fc455 (updated class api took out calendar code)
    max_users = models.IntegerField(default=6)
    time = models.DateTimeField(default=now)
    description = models.TextField(max_length=250, default='', blank=True)

class Message(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user_message", on_delete=models.CASCADE )
    to_user = models.ForeignKey(User, related_name="to_user_message", on_delete=models.CASCADE )
    msg_content = models.CharField(max_length = 200, unique = True)

    def str(self):
        return f"From {self.from_user.username} to {self.to_user.username}: {self.msg_content}"
=======
#
# class CredentialsModel(models.Model):
#     id = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
#     credential = CredentialsField()
#     task = models.CharField(max_length=80, null=True)
#     updated_time = models.CharField(max_length=80, null=True)
<<<<<<< HEAD

>>>>>>> 6db00cf (add requirements.txt)
=======
#
# class CredentialsAdmin(admin.ModelAdmin):
#     pass
>>>>>>> 7205032 (fixing calendar file)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('profile saved')
    instance.userprofile.save()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE )
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE )

    def __str__(self):
        return f"Request from {self.from_user.username} to {self.to_user.username}"