"""
File: mini_fb/models.py
Author: Winson Dong (winson@bu.edu)
Description:
    Defines database models for Profile, StatusMessage, Image, StatusImage, and Friend.
"""

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    first = models.TextField(blank=False)
    last = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    profile_image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.first} {self.last}"
    
    def get_status_messages(self):
        '''Return all status messages for this profile'''

        messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return messages
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_friends(self):
        
        # Get Friend objects where it's either profile1 or profile2
        friends_profile1 = Friend.objects.filter(profile1=self)
        friends_profile2 = Friend.objects.filter(profile2=self)

        friend_profiles = []

        for friend in friends_profile1:
            friend_profiles.append(friend.profile2)

        for friend in friends_profile2:
            friend_profiles.append(friend.profile1)

        return friend_profiles
    

    def add_friend(self, other):
        ''' to add friend between two Profile'''
        existing_friendship = Friend.objects.filter(profile1=self, profile2=other).exists() or Friend.objects.filter(profile1=other, profile2=self).exists()

        if not existing_friendship:
            friendship = Friend(profile1=self, profile2=other)
            friendship.save()

    
    def get_friend_suggestions(self):
        possible_friends = set()

        direct_friends = set(self.get_friends())
        for friend in direct_friends:
            for fof in friend.get_friends(): # get friends of friends
                if fof != self and fof not in direct_friends:
                    possible_friends.add(fof)
        
        return list(possible_friends) 
    

    def get_news_feed(self):

        friends = self.get_friends()
        profiles = friends + [self]
        news_feed = StatusMessage.objects.filter(profile__in=profiles).order_by('-timestamp')
    
        return news_feed

        
class StatusMessage(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)

    def __str__(self):
        return f"{self.profile}: {self.message} {self.timestamp}"
    
    def get_images(self):
        return StatusImage.objects.filter(status_message=self)
    

class Image(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    image_file =  models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self): 
        return f"Image uploaded by: {self.profile} on {self.timestamp}"
    

class StatusImage(models.Model):
    image = models.ForeignKey("Image", on_delete=models.CASCADE)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Image {self.image} linked to StatusMessage {self.status_message}"
    

class Friend(models.Model):
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1} and {self.profile2}"
    
    