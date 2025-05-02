"""
File: project/models.py
Author: Winson Dong (winson@bu.edu)
Description:
    Defines the core data models for the Restaurant Reservation system:
    - Restaurant: stores menu-less restaurant details and address
    - Customer: extends Django User with profile data
    - Table: represents seating tables for each restaurant
    - Reservation: ties customers to tables at specific times

Each model includes __str__ methods for readable representations,
reverse methods where appropriate, and comments explaining fields.
"""


from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Restaurant(models.Model):
    """
    A dining location offering tables for reservation.
    Fields:
      - restaurant_name: the display name of the restaurant
      - cuisine: type of food (choice from CUISINE_CHOICES)
      - address fields: street number, street name, city, state, zip
      - restaurant_number: phone contact
      - opening_hours: textual representation of hours
    """
    CUISINE_CHOICES = [
        ("american", "American"),
        ("chinese", "Chinese"),
        ("italian", "Italian"),
        ("japanese", "Japanese"),
        ("mexican", "Mexican"),
        ("indian", "Indian"),
        ("thai", "Thai"),
        ("french", "French"),
        ("greek", "Greek"),
        ("mediterranean", "Mediterranean"),
    ]

    restaurant_name = models.TextField(blank=False)
    cuisine = models.TextField(choices=CUISINE_CHOICES, blank=False)

    # restaurant address
    restaurant_street_number = models.IntegerField(blank=False)
    restaurant_street_name = models.TextField(blank=False)
    restaurant_city = models.TextField(blank=False)
    restaurant_state = models.TextField(blank=False)
    restaurant_zip_code = models.IntegerField(blank=False)

    restaurant_number = models.TextField(blank=False)
    opening_hours = models.TextField(blank=False)

    def __str__(self):
        return f"{self.restaurant_name}"
    
class Customer(models.Model):
    """
    Profile extension for Django's built-in User.
    Fields:
      - user: One-to-many link to Django User
      - first_name, last_name
      - email: validated EmailField
      - phone_number: free-form text
      - profile_image: optional uploaded picture
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.TextField(blank=False)
    profile_image =  models.ImageField(blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_success_url(self):
        """
        Redirect to the customer's own profile page.
        """
        return reverse('reservation_success', args=[self.object.pk])

    

class Table(models.Model):
    """
    A seating table within a Restaurant.
    - restaurant: FK back to Restaurant
    - table_number: identifier like "A1" or "B2"
    - seating_capacity: number of people the table can hold
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    table_number = models.CharField(max_length=10)
    seating_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.table_number} at {self.restaurant.restaurant_name}"
    

class Reservation(models.Model):
    """
    A booking of a specific Table by a Customer at a Restaurant.
    Fields:
      - restaurant: FK back to Restaurant
      - customer: FK back to Customer
      - table: FK back to Table
      - reservation_date, reservation_time: when the booking occurs
      - party_size: number of seats requested
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField()

    def __str__(self):
        return f"Reservation at {self.restaurant.restaurant_name} for {self.customer} on {self.reservation_date} at {self.reservation_time}"



    



