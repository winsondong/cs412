"""
File: mini_fb/forms.py
Author: Winson Dong (winson@bu.edu)
Description:
    Defines forms for user input validation.
"""


from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    ''' A form to create a Profile to the database '''
    
    class Meta:
        ''' associate this form to the model in our database '''
        model = Profile
        fields = ["first", "last", "city", "email_address", "profile_image_url"]


class CreateStatusMessageForm(forms.ModelForm):
    ''' A form to create a StatusMessage to the database '''
    class Meta:
        ''' associate this form to the model in our database '''
        model = StatusMessage
        fields = ["message"]


class UpdateProfileForm(forms.ModelForm):
    ''' A form to update a profile '''
    class Meta:
        ''' associate this form to the model in our database '''
        model = Profile
        fields = ["city", "email_address", "profile_image_url"]
        

class UpdateStatusMessageForm(forms.ModelForm):
    ''' A form to update a status message'''
    class Meta:
        ''' associate this form to the model in our database '''
        model = StatusMessage
        fields = ["message"]

