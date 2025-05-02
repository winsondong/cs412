"""
File: project/forms.py
Author: Winson Dong (winson@bu.edu)
Description:
    Defines forms for user input validation.
"""


from django import forms
from .models import Reservation, Customer

class ReservationForm(forms.ModelForm):
    ''' A form to create a Reservation to the database '''
    
    class Meta:
        ''' associate this form to the Reservation model in our database '''
        model = Reservation
        fields = ["table", "reservation_date", "reservation_time", "party_size"]
        widgets = {
            # Plain text field with JS datepicker attached
            'reservation_date': forms.TextInput(attrs={'id': 'datepicker'}),
            # HTML5 time input for browser-native picker
            'reservation_time': forms.TimeInput(attrs={'type': 'time'}),
            # Number input with a minimum of 1
            'party_size': forms.NumberInput(attrs={'min': 1}),
            # Hidden input so user cannot change once chosen
            'table': forms.HiddenInput(),
        }

class CustomerForm(forms.ModelForm):
    """
    Form for new Customer registration.
    Collects first/last name, email, phone, and optional profile image.
    Paired with Django's UserCreationForm in the registration view.
    """

    class Meta:
        ''' associate this form to the Customer model in our database'''
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']


class EditCustomerForm(forms.ModelForm):
    """
    Form for editing existing Customer profile.
    Same fields as registration but used in UpdateView.
    """

    class Meta:
        ''' associate this form to the Customer model in our database '''
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
