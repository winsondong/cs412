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

        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    
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
    
    
