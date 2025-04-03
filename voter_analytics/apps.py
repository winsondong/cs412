"""
File: voter_analytics/apps.py
Author: Winson Dong (winson@bu.edu)
Description:
    Configures the voter_analytics app.
"""

from django.apps import AppConfig


class VoterAnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voter_analytics'
