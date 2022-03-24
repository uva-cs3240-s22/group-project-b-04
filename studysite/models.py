from operator import truediv
from django.db import models

# Create your models here.

class classes(models.Model):
    classes_text = models.CharField(max_length = 9, unique = True)
    def __str__(self):
        return self.classes_text
