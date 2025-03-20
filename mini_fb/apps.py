"""
File: mini_fb/apps.py
Author: Winson Dong (winson@bu.edu)
Description:
    Configures the mini_fb app.
"""

from django.apps import AppConfig


class MiniFbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mini_fb'
