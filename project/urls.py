"""
File: project/urls.py
Author: Winson Dong (winson@bu.edu)
Description:
    Maps URLs to views for the project app.
"""


from django.urls import path
from .views import *



urlpatterns = [
    # map the URL (empty string) to the view
    path('', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurant/<int:pk>/reserve', ReservationCreateView.as_view(), name='restaurant_reservation'),
    
]