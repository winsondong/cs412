from django.db import models

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
    
    
class StatusMessage(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=False)
    message = models.TextField(blank=False)

    def __str__(self):
        return f"{self.profile}: {self.message} {self.timestamp}"
    



