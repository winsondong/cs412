
from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
