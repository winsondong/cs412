"""
File: project/models.py
Author: Winson Dong (winson@bu.edu)
Description:
    Defines database models for Restaurant, Customer, Table,  Reservation
"""


from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Restaurant(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.TextField(blank=False)
    profile_image =  models.ImageField(blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('restaurant_list')
    

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
    table_number = models.CharField(max_length=10)
    seating_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Table {self.table_number} at {self.restaurant.restaurant_name}"
    

class Reservation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField()

    def __str__(self):
        return f"Reservation at {self.restaurant.restaurant_name} for {self.customer} on {self.reservation_date} at {self.reservation_time}"



    



