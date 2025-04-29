"""
File: project/views.py
Author: Winson Dong (winson@bu.edu)
Description:
    
"""

from .models import Restaurant, Customer, Table, Reservation
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView
from .forms import ReservationForm, CustomerForm, EditCustomerForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy



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
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])
        form.instance.restaurant = restaurant
        return super().form_valid(form)
        

class RegistrationCreateView(CreateView):
    ''' A view to handle creation of a customer '''

    model = Customer
    form_class = CustomerForm
    template_name = 'project/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context
    

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Customer object.
        '''
        # UserCreationForm instance from the self.request.POST data
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            # saving the user and getting the user instance
            user = user_form.save()

            form.instance.user = user

            # login after creation
            login(self.request, user)

            return super().form_valid(form)
        
        return super().form_invalid(form)
    
    def get_success_url(self):

        return reverse('customer_profile')
    

class CustomerProfileDetailView(LoginRequiredMixin, DetailView):
    ''' A view to display the customer's profile page '''

    model = Customer
    template_name = 'project/customer_profile.html'
    context_object_name = 'customer'

    def get_object(self):

        return get_object_or_404(Customer, user=self.request.user)
    

class EditCustomerUpdateView(LoginRequiredMixin, UpdateView):
    ''' A view to update the customer's profile page '''
    model = Customer
    form_class = EditCustomerForm
    template_name = 'project/edit_profile.html'

    def get_object(self):
        
        return get_object_or_404(Customer, user=self.request.user)
    
    def get_success_url(self):
        # you could even build it off self.object.pk
        return reverse_lazy('customer_profile')
    


    

    