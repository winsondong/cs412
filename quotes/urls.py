from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # Example route (you can modify this later)
    path('', views.index, name='index'),
]
