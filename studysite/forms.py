from .models import *
from django import forms

#Learned about formatting of forms in forms.py in https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/#:~:text=instance.profile.save%20%28%29%20You%20can%20get%20confused%20from%20this,The%20other%20method%20save_profile%20just%20saves%20the%20instance.
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['year', 'major', 'bio', 'image']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'question']