"""
File: project/views.py
Author: Winson Dong (winson@bu.edu)
Description:
    All view logic for the Restaurant Reservation application:
    - Listing and filtering restaurants
    - Displaying restaurant details and available tables
    - User registration and login
    - Creating, editing, deleting Reservations
    - Viewing and editing Customer profiles

"""

from .models import Restaurant, Customer, Table, Reservation
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ReservationForm, CustomerForm, EditCustomerForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render
from django.urls import reverse



class RestaurantListView(ListView):
    """
    Display a list of all restaurants, optionally filtered by cuisine.
    - GET: renders 'restaurant_list.html' with 'restaurants' and 'cuisines'.
    """

    model = Restaurant
    template_name = 'project/restaurant_list.html'
    context_object_name = 'restaurants'


    def get_context_data(self, **kwargs):
        """
        Add a distinct list of cuisines for the filtering UI.
        """
        context = super().get_context_data(**kwargs)

        # get distinct cuisine values
        cuisines = Restaurant.objects.order_by('cuisine').values_list('cuisine', flat=True).distinct()
        context['cuisines'] = cuisines
        return context


    def get_queryset(self):
        """
        Optionally filter restaurants by the 'cuisine' GET parameter.
        """

        result = super().get_queryset()
        cuisine = self.request.GET.get('cuisine')

        if cuisine:
            result = result.filter(cuisine=cuisine)
        
        return result


class RestaurantDetailView(DetailView):
    """
    Show details for a single restaurant and its available tables,
    sorted alphabetically by table number.
    """

    model = Restaurant
    template_name = 'project/restaurant_detail.html'
    context_object_name = 'restaurant'

    def get_context_data(self, **kwargs):
        """
        Handle new Customer registration alongside Django's UserCreationForm.
        - Displays combined form (customer + user credentials)
        - Saves User first, then associates Customer to that user.
        """
        context = super().get_context_data(**kwargs)

        # grab the restaurant object
        restaurant = context['restaurant']

        # instead of using restaurant.tables.all() in the template,
        # hand in a sorted queryset
        context['tables'] = restaurant.tables.all().order_by('table_number')
        return context


class RegistrationCreateView(CreateView):
    """
    Add a UserCreationForm instance to the context alongside CustomerForm.
    """

    model = Customer
    form_class = CustomerForm
    template_name = 'project/registration.html'

    def get_context_data(self, **kwargs):
        """
        Add a UserCreationForm instance to the context alongside CustomerForm.
        """
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        """
        On valid POST, save the User first, then tie the new Customer to it,
        and log the user in.
        """
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
        """
        Redirect to the customer's profile page after registration.
        """
        return reverse('customer_profile')


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """
    Allow authenticated users to make a reservation:
    - Pre-fill table selection via the 'table' GET param
    - Hide table field, enforce seat-capacity limit on party size
    """

    model = Reservation
    form_class = ReservationForm
    template_name = 'project/restaurant_reservation_form.html'

    def get_context_data(self, **kwargs):
        """
        Gather restaurant and selected table info; build seat_range for dropdown.
        """
        context = super().get_context_data(**kwargs)
        restaurant_pk = self.kwargs['pk']
        context['restaurant'] = Restaurant.objects.get(pk=restaurant_pk)

        table_id = self.request.GET.get('table')
        if table_id:
            table = get_object_or_404(Table, pk=table_id, restaurant=restaurant_pk)
            context["selected_table"] = table
            context['seat_range'] = range(1, table.seating_capacity + 1)
        return context
    
    # pull the ?table=XXX off the URL and stick it into initial
    def get_initial(self):
        """
        Pre-populate the hidden 'table' field from ?table=ID.
        """
        initial = super().get_initial()
        table_id = self.request.GET.get('table')
        if table_id:
            initial['table'] = table_id
        return initial
    
    def form_valid(self, form):
        """
        Attach the current restaurant and customer to the reservation before saving.
        """
        restaurant = Restaurant.objects.get(pk=self.kwargs['pk'])
        form.instance.restaurant = restaurant

        form.instance.customer = Customer.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        After save, redirect to a confirmation page showing the new reservation.
        """
        # self.object is the new Reservation instance
        return reverse('reservation_success', kwargs={'pk': self.object.pk})
    


def reservation_success(request, pk):
    """
    Render a simple confirmation page with the newly created Reservation.
    """
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request,'project/reservation_success.html', {'reservation': reservation})


class ReservationEditView(LoginRequiredMixin, UpdateView):
    """
    Let users edit an existing reservation's date/time/party size.
    Ensures only the owner can update, and reuses seat_range logic.
    """
    model = Reservation
    form_class = ReservationForm
    template_name = 'project/reservation_edit_form.html'

    def get_queryset(self):
        """
        Restrict edits to reservations owned by the current user.
        """
        # only allow users to edit their own reservations
        return super().get_queryset().filter(customer__user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """
        Add restaurant, table, and seat_range for the edit template.
        """
        context = super().get_context_data(**kwargs)
        reservation = self.get_object()
        context['restaurant'] = reservation.restaurant
        context['selected_table'] = reservation.table
        context['seat_range'] = range(1, reservation.table.seating_capacity + 1)
        return context
    

    def get_initial(self):
        """ Get the table """
        initial = super().get_initial()
        table_id = self.request.GET.get('table')
        if table_id:
            initial['table'] = table_id
        return initial

    def get_success_url(self):
        ''' Return the URL to which we should be directed after the delete. '''

        # reverse to show the Profile page
        return reverse('customer_profile')


class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    """
    Allow users to cancel (delete) their own reservations.
    Presents a confirmation template, then redirects home.
    """
    model = Reservation
    template_name = 'project/reservation_confirm_delete.html'
    context_object_name = 'reservation'

    def get_queryset(self):
        """
        Only let the owning user delete their reservation.
        """
        # only allow deleting your own reservations
        return super().get_queryset().filter(customer__user=self.request.user)

    def get_success_url(self):
        """
        Redirect back to the customer profile after deletion.
        """

        # reverse to show the Profile page
        return reverse('customer_profile')
    


class CustomerProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Show the logged-in user's profile and their upcoming reservations.
    """

    model = Customer
    template_name = 'project/customer_profile.html'
    context_object_name = 'customer'

    def get_object(self):
        """
        Fetch the Customer linked to the current User.
        404 if missing.
        """
        return get_object_or_404(Customer, user=self.request.user)
    
    def has_reservation(self):
        """
        Returns True if this customer has at least one reservation
        """
        return Reservation.objects.filter(customer=self.get_object()).exists()

    def get_context_data(self, **kwargs):
        """
        Add 'reservations' queryset and a boolean flag to the template.
        """
        context = super().get_context_data(**kwargs)
        customer_obj = self.get_object()
        reservations = Reservation.objects.filter(customer=customer_obj).order_by('reservation_date', 'reservation_time')
        context['has_reservation'] = self.has_reservation()
        context['reservations'] = reservations

        return context
    

class EditCustomerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Enable users to update their own Customer profile information.
    """
    model = Customer
    form_class = EditCustomerForm
    template_name = 'project/edit_profile.html'

    def get_object(self):
        """
        Return the Customer instance tied to the current user.
        """
        return get_object_or_404(Customer, user=self.request.user)
    
    def get_success_url(self):
        """
        Return to the customer profile page after saving edits.
        """
        return reverse('customer_profile')
    



    

    