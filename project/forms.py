"""
File: project/forms.py
Author: Winson Dong (winson@bu.edu)
Description:
    Defines forms for user input validation.
"""


from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    ''' A form to create a Reservation to the database '''
    
    class Meta:
        ''' associate this form to the Reservation model in our database '''
        model = Reservation
        fields = ["table", "reservation_date", "reservation_time", "party_size"]

