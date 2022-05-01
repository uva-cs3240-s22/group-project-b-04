from .models import *
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['year', 'major', 'bio', 'image']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['first_name', 'last_name', 'email', 'question']