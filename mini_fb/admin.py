"""
File: mini_fb/admin.py
Author: Winson Dong (winson@bu.edu)
Description:
    Registers models for the Django admin panel.
"""

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage, Friend
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)
