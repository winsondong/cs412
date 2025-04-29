"""
File: project/urls.py
Author: Winson Dong (winson@bu.edu)
Description:
    Maps URLs to views for the project app.
"""


from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views



urlpatterns = [
    # map the URL (empty string) to the view
    path('', RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurant/<int:pk>', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurant/<int:pk>/reserve', ReservationCreateView.as_view(), name='restaurant_reservation'),
    path('restaurant/register_account', RegistrationCreateView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='project/restaurant_list.html'), name='logout'), 
    path('customer/profile/', CustomerProfileDetailView.as_view(), name='customer_profile'),
     path('customer/profile/edit/', EditCustomerUpdateView.as_view(), name='edit_profile'),

]