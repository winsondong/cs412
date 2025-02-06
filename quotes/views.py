# quotes/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def main(request):
    ''' Fund to respond to the "main" request '''

    response_text = '''
    <html>
    <h1>Hello, world!</h1>
    </html>

    '''

    return HttpResponse(response_text)
