from django.http import HttpResponse
import requests
from django.shortcuts import render
from .models import Mobile
from bs4 import BeautifulSoup





def index(request):

    #MercadolibreApi()
    EbayApi()
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

def KimovilScraping():
    print ("hola")



def MercadolibreApi():
    brands = ['Oneplus' , 'Xiaomi', 'Own', 'ZTE' , 'Huawei']
    brands = {'Oneplus': 'MLC157416' , 'Xiaomi' : 'MLC157415', 'Own' : 'MLC174007', 'Huawei' : 'MLC157425' , 'ZTE' : 'MLC157421' }
    categories = requests.get('https://api.mercadolibre.com/categories/MLC1055')
    categories_data = categories.json()

    product_by_category = requests.get('https://api.mercadolibre.com/sites/MLC/search?category=MLC157416')
    all_products = product_by_category.json()

    print (all_products['results'][0]['title'])

    response = requests.get('https://api.mercadolibre.com/items/MLC497664741')
    data = response.json()

    shop = requests.get('https://api.mercadolibre.com/users/166687136')
    shop_data = shop.json()
    shop_name = shop_data['nickname']



def EbayApi():

    product = requests.get('https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=DiegoTar-TallerWe-PRD-ddfb0df12-769800d3&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&aspectFilter.aspectName=Brand&aspectFilter.aspectValueName=Xiaomi&itemFilter(0).name=Condition&itemFilter(0).value=New&categoryId=9355')
    product_data = product.json()



    print (product_data)


