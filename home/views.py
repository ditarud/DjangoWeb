from django.http import HttpResponse
import requests
from django.shortcuts import render
from .models import Mobile




def index(request):

    response = requests.get('https://mindicador.cl/api')
    data = response.json()

    dolar = data['dolar']['valor']
    mobiles = Mobile.objects.all()[0]

    context = {'valor_dolar':dolar, 'mobiles':mobiles}


    return render( request, 'search.html', context)
