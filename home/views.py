from django.http import HttpResponse
import requests
from django.shortcuts import render
from .models import Mobile
from bs4 import BeautifulSoup





def index(request):


    mobiles = Mobile.objects.all()[0]

    context = {'valor_dolar':DolarApi(), 'mobiles':mobiles}

    return render( request, 'search.html', context)


def DolarApi():
    response = requests.get('https://mindicador.cl/api')
    data = response.json()

    dolar = data['dolar']['valor']
    return dolar

def PromovilScraping(request):
    brands = ['40-oneplus', '69-huawei', '105-xiaomi', '15-samsung']

    for brand in brands:
        website =  "https://www.promovil.cl/brand"
        url = website.replace("brand", brand)
        source = requests.get(url)
        soup = BeautifulSoup(source.content,"lxml")

        summary = soup.find_all('article', {"class": "product-miniature js-product-miniature"})
        brand = brand.split("-")[1]

        for item in summary:

           model =  (item.find_all("a", {"class": "product_name"})[0].text)
           price = (item.find_all("span", {"class": "price"})[0].text)
           link =  (item.find_all("a", {"class": "thumbnail product-thumbnail"})[0]['href'])



           mobile = Mobile.objects.get_or_create(brand=brand, release_date="", price=price, model=model, screen_size=0, resolution="", dimensions="", weight=0, ram="",
                                          storage="",rear_camera="",front_camera="",score="",shop="Promovil",link=link)
    return render(request,'scraping.html')