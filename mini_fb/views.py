from django.shortcuts import render
from .models import Profile
from django.views.generic import ListView, DetailView, CreateView
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse


# Create your views here.

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all profiles.'''

    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ShowProfilePageView(DetailView):
    '''Show the details for one profile.'''

    model = Profile 
    template_name = 'mini_fb/show_profile.html' 
    context_object_name = 'profile' 

class CreateProfileView(CreateView):
    '''A view to handle creation of a new Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Profile object (POST)
    '''
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'


class CreateStatusMessageView(CreateView):
    '''A view to handle creation of a new StautsMessage.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new StatusMessage object (POST)
    '''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        pk = self.kwargs['pk']

        # call reverse to generate the URL for this Profile
        return reverse('show_profile', kwargs={'pk': pk})


    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the StatusMessage
        object before saving it to the database.
        '''
        
		# instrument our code to display form fields: 
        print(f"CreateCommentView.form_valid: form.cleaned_data={form.cleaned_data}")
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this profile to the status message
        form.instance.profile = profile # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)




    
    