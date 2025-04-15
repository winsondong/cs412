"""
File: project/apps.py
Author: Winson Dong (winson@bu.edu)
Description:
    Configures the project app.
"""
from django.apps import AppConfig


class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'
