# quotes/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.

quotes = [
    "Float like a butterfly, sting like a bee. You can't hit what your eyes don't see.",
    "The man who has no imagination has no wings.",
    "I'm young; I'm handsome; I'm fast. I can't possibly be beat."
]

images = [
    "/static/imgs/muhammad-ali-1.jpg",
    "/static/imgs/muhammad-ali-2.jpg",
    "/static/imgs/muhammad-ali-3.jpg",
    "/static/imgs/muhammad-ali-profile-image.jpg"
]



def base_page(request):
    '''Respond to the URL '', delegate work to a template'''

    template_name = 'quotes/base.html'
    
    return render(request, template_name)

def quote_page(request):
    ''' Getting a random quotes and images to the template'''

    template_name = 'quotes/quote.html'

    random_quote = random.choice(quotes)
    random_image = random.choice(images)

    context = {
        "quote": random_quote,
        "image": random_image,

    }

    return render(request, template_name, context)

def show_all_page(request):
    ''' Pass all quotes and images to the template'''

    template_name = 'quotes/show_all.html'
    context = {
        "quote": quotes,  
        "image": images 
    }
    
    return render(request, template_name, context)

def about_page(request):
    ''' About Muhammad Ali'''

    template_name = 'quotes/about.html'

    context = {
        "profile_pic": "/static/imgs/muhammad-ali-profile-image.jpg"
    }

    

    return render(request, template_name, context)


