"""
File: project/views.py
Author: Winson Dong (winson@bu.edu)
Description:
    
"""

from .models import Restaurant, Customer, Table, Reservation
from django.views.generic import View, ListView, DetailView, CreateView
from .forms import ReservationForm


class RestaurantListView(ListView):
    '''Create a subclass of ListView to display all restaurants.'''

    model = Restaurant
    template_name = 'project/restaurant_list.html'
    context_object_name = 'restaurants'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get distinct cuisine values
        cuisines = Restaurant.objects.order_by('cuisine').values_list('cuisine', flat=True).distinct()
        context['cuisines'] = cuisines
        return context


    def get_queryset(self):
        result = super().get_queryset()
        cuisine = self.request.GET.get('cuisine')

        if cuisine:
            result = result.filter(cuisine=cuisine)
        
        return result


class RestaurantDetailView(DetailView):
    '''Show the details for one restaurant.'''

    model = Restaurant
    template_name = 'project/restaurant_detail.html'
    context_object_name = 'restaurant'


class ReservationCreateView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''
    model = Reservation
    form_class = ReservationForm
    template_name = 'project/restaurant_reservation_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        restaurant_pk = self.kwargs['pk']
        context['restaurant'] = Restaurant.objects.get(pk=restaurant_pk)

        return context
    
    def form_valid(self, form):
        ''' associating the reservation to the restaurant '''
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])
        form.instance.restaurant = restaurant

        return super().form_valid(form)
    

    