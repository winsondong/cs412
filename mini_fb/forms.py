# creates the form model for each of the forms of the app. One for creating a profile and 
# for creating a status message

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
