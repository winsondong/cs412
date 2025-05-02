"""
File: mini_fb/views.py
Author: Winson Dong (winson@bu.edu)
Description:
    Handles requests, renders templates, and processes user actions.
"""


from django.shortcuts import render, redirect
from .models import Profile, StatusMessage, Image, StatusImage
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



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
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = UserCreationForm()
        return context
    

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
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


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new StautsMessage.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new StatusMessage object (POST)
    '''
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'


    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        # pk = self.kwargs['pk'] #OLD
        # profile = Profile.objects.get(pk=pk) #OLD
        context['profile'] = Profile.objects.get(user=self.request.user)
        # add this profile into the context dictionary:
        # context['profile'] = profile
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
        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)
        profile = self.get_object()
        # attach this profile to the status message
        form.instance.profile = profile # set the FK

        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files:
            # Create an Image object
            image = Image(profile=profile, image_file=file)
            image.save()

            # Create an StatusImage object
            status_image = StatusImage(image=image, status_message=sm)
            status_image.save()

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to redirect to after successfully submitting form.'''
       
        return self.object.profile.get_absolute_url()
    

    def get_login_url(self):
        ''' custom URL '''
        return reverse("login")
    

    def get_object(self):

        return Profile.objects.get(user=self.request.user)
    


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to handle updating an existing Profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and update the existing Profile object (POST).
    '''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'

    def get_login_url(self):
        ''' custom URL '''
        return reverse("login")

    def get_object(self):

        return Profile.objects.get(user=self.request.user)
    

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a StatusMessage.'''

    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        ''' Return the URL to which we should be directed after the delete. '''

        # getting the pk for this status message
        pk = self.kwargs.get('pk')

        # find the StatusMessage object
        status_message = StatusMessage.objects.get(pk=pk)

        # find the Profile that this StatusMessage relate to 
        profile = status_message.profile  

        # reverse to show the Profile page
        return reverse('show_profile', kwargs={'pk': profile.pk})

    def get_login_url(self):
        ''' custom URL '''
        return reverse("login")
    

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    ''' A view to update a StatusMessage '''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = 'mini_fb/update_status_form.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['profile'] = self.object.profile  # Add profile to context
        return context

    def get_success_url(self):
            ''' Return the URL to which we should be directed after the delete. '''

            # getting the pk for this status message
            pk = self.kwargs.get('pk')

            # find the StatusMessage object
            status_message = StatusMessage.objects.get(pk=pk)

            # find the Profile that this StatusMessage relate to 
            profile = status_message.profile  

            # reverse to show the Profile page
            return reverse('show_profile', kwargs={'pk': profile.pk})

    def get_login_url(self):
        ''' custom URL '''
        return reverse("login_mfb")
    

class AddFriendView(LoginRequiredMixin, View):
    ''' A view to add friend '''

    def dispatch(self, request, *args, **kwargs):
        # get the logged-in user's profile
        profile = Profile.objects.get(user=request.user)

        # get the other profile by PK
        other_profile_pk = kwargs['other_pk']
        other_profile = Profile.objects.get(pk=other_profile_pk)

        # call add_friend
        profile.add_friend(other_profile)

        return redirect('show_profile', pk=profile.pk)
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


    def get_login_url(self):
        ''' custom URL '''
        return reverse("login_mfg")
    

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    ''' A view to show friend suggestions '''
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    

    def get_login_url(self):
        ''' custom URL '''
        return reverse("login_mfb")


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    ''' A view to show news feed '''
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    

    def get_login_url(self):
        ''' custom URL '''
        return reverse("login_mfb")
    