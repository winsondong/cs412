"""
File: project/admin.py
Author: Winson Dong (winson@bu.edu)
Description:
    Registers models for the Django admin panel.
"""

from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Table)
admin.site.register(Reservation)
