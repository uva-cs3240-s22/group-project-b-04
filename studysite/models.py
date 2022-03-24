from operator import truediv
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# If the User model is constomized we need to change how we set up User
    #from django.contrib.auth import get_user_model
    #User = get_user_model()
class classes(models.Model):
    classes_text = models.CharField(max_length = 9, unique = True)
    roster = models.ManyToManyField(User)
    def __str__(self):
        return self.classes_text
