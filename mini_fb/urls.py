# mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', ShowProfilePageView.as_view(), name='show_profile')
]