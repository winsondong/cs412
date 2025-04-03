"""
File: voter_analytics/urls.py
Author: Winson Dong (winson@bu.edu)
Usage:
    Maps URLs to views for the voter_analytics app.
"""

from django.urls import path
from .views import *

urlpatterns = [
    # map the URL (empty string) to the view
	path('', VoterListView.as_view(), name='home'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphListView.as_view(), name='graphs'),
]