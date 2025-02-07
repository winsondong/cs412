from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # Example route (you can modify this later)
    path(r'', views.quote_page, name="base_page"),
    path(r'quote', views.quote_page, name="quote_page"),
    path(r'show_all', views.show_all_page, name="show_all_page"),
    path(r'about', views.about_page, name="about_page"),

]
