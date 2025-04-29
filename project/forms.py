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
            'reservation_date': forms.TextInput(attrs={'id': 'datepicker'}),
            'reservation_time': forms.TimeInput(attrs={'type': 'time'}),
            'party_size': forms.NumberInput(attrs={'min': 1}),
        }

class CustomerForm(forms.ModelForm):
    ''' A form to put take in Customer info '''

    class Meta:
        ''' associate this form to the Customer model in our database'''
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']


class EditCustomerForm(forms.ModelForm):
    ''' A form to edit customer info'''

    class Meta:
        ''' associate this form to the Customer model in our database '''
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'profile_image']
