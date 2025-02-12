# quotes/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime, timedelta

import time
import random
import pytz  # Import timezone support


# Create your views here.

daily_specials = {
    "General Tso's Chicken Combo": "Crispy fried chicken in a tangy-sweet sauce, served with rice and an egg roll.",
    "Honey Walnut Shrimp Plate": "Lightly battered shrimp coated in a creamy honey glaze, topped with candied walnuts.",
    "Mongolian Beef Bowl": "Tender beef stir-fried with green onions and a savory brown sauce, served over rice.",
    "Orange Chicken & Lo Mein Combo": "Crispy orange chicken paired with stir-fried lo mein noodles and mixed veggies.",
}


menu_item_names = {
    "chicken-broccoli": {"name": "Chicken w/ Broccoli ($10)", "has_options": True, "price": 10},
    "beef-broccoli": {"name": "Beef w/ Broccoli ($10)", "has_options": True, "price": 10},
    "crab-rangoon": {"name": "Crab Rangoon ($5)", "has_options": False, "price": 5},
    "egg-roll": {"name": "Egg Roll ($2)", "has_options": False, "price": 2}
}

def base_page(request):
    '''Respond to the URL '', delegate work to a template'''

    template_name = 'restaurant/base.html'
    
    return render(request, template_name)

def main_page(request):
    '''Respond to the url /main, includes name, location, hours of operation, and one or more photos'''
    
    template_name = 'restaurant/main.html'

    return render(request, template_name)

def order_page(request):
    '''Respond to the url /order, display an online order form'''
    
    template_name = 'restaurant/order.html'

    
    special_name = random.choice(list(daily_specials.keys()))
    special_description = daily_specials[special_name]

    context = {
        "special_name": special_name,
        "special_description": special_description,
        "menu_items": menu_item_names
    }

    return render(request, template_name, context)

def confirmation_page(request):
    '''Respond to the url /confirmation, display an online order confirmation of user's input.'''
    
    template_name = 'restaurant/confirmation.html'
    
     # check if POST data was sent with the HTTP POST message:
    if request.POST:

        # extract form fields into variables
        
        # get a list of selected items
        selected_items = request.POST.getlist('menu-items')
        selected_special = request.POST.get('daily-special')
        menu_items = []
        total_price = 0

        for item in selected_items:
            item_info = menu_item_names.get(item, {})  # Get item details
            item_name = item_info.get("name")
            item_price = item_info.get("price")

            spice_level = request.POST.get(f"{item}-spice")
            if spice_level and spice_level != "none":
                item_name += f" (Spice: {spice_level})"

            menu_items.append(item_name)
            total_price += item_price
        


        special_instructions = request.POST['special-instructions']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

        get_tz = pytz.timezone('America/New_York')  # get correct time zone
        current_time = datetime.now(pytz.utc).astimezone(get_tz)  # get current time in UTC and convert it to New York time
        ready_time = current_time + timedelta(minutes=random.randint(30, 60)) # add 30-60 minutes of time to current time
        formatted_ready_time = ready_time.strftime("%b. %d, %Y, %I:%M %p")  # formating the time to month, day, year, hour:, minute, PM

        context = {
            
            "menu_items": menu_items,
            "daily_special": selected_special,
            "special_instructions": special_instructions,
            "total_price": total_price,
            "name": name,
            "phone": phone,
            "email": email,
            "ready_time": formatted_ready_time
            

        }

    # delegate the response to the template, provide context variables
    return render(request,  template_name, context)