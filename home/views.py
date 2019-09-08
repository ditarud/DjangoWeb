from django.http import HttpResponse
import requests
from django.shortcuts import render
from .models import Mobile
from bs4 import BeautifulSoup
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    mobiles = Mobile.objects.all()[0]
    list_mobiles  = Mobile.objects.filter(Q(model__contains='one plus') | Q(model__contains='oneplus'))[:20]
    paginator = Paginator(list_mobiles, 6)

    page = request.GET.get('page')

    list_mobiles = paginator.get_page(page)

    context = {'valor_dolar':DolarApi(), 'mobiles':mobiles, 'list_mobiles': list_mobiles}
    #getAllExactModelName()
    #getLinkFromBD()
    #KimovilScraping()
    #checkScore()


    return render( request, 'search.html', context)


def getAllExactModelName():
    mobile_models = Mobile.objects.filter(Q(model__contains='one plus') | Q(model__contains='oneplus'))
    count_oneplus = Mobile.objects.filter(Q(brand="OnePlus") | Q(brand="oneplus")).count()
    count = 0
    all_oneplus_models = []
    all_xiaomi_models = []
    all_huawei_models = []
    all_oppo_models = []
    all_zte_models = []
    for i in mobile_models:
        list_of_words = i.model.split()
        for k in list_of_words:
           if k == 'oneplus' and len(list_of_words) > 2:
               next_word = list_of_words[list_of_words.index('oneplus') + 1] + " " + list_of_words[list_of_words.index('oneplus') + 2]
               all_oneplus_models.append(next_word)
           if k == 'one plus' and len(list_of_words) > 2:
               next_word = list_of_words[list_of_words.index('one plus') + 1] + " " + list_of_words[
                   list_of_words.index('one plus') + 2]
               all_oneplus_models.append(next_word)
           if k == 'One Plus' and len(list_of_words) > 2:
               next_word = list_of_words[list_of_words.index('One Plus') + 1] + " " + list_of_words[
                   list_of_words.index('One Plus') + 2]
               all_oneplus_models.append(next_word)
           if k == 'ONEPLUS' and len(list_of_words) > 2:
               next_word = list_of_words[list_of_words.index('ONEPLUS') + 1] + " " + list_of_words[
                   list_of_words.index('ONEPLUS') + 2]
               all_oneplus_models.append(next_word)

    count+=1
    print ((all_oneplus_models))
    return all_oneplus_models
    # SACAR DE LA BD TODOS LOS MODELOS QUE TENEMOS , PARA EMPEZAR A JUNTAR COSAS Y PODER BUSCAR EN KIMOVIL CON SCRAPING
    # RETORNAR UNA LISTA CON TODOS LOS MODELOS COMO [MI9,MI8,6T,7PRO,7,REDMI,A1,A2,A3,MATE20,MATE30,ETC]


def getLinkFromBD():
    mobile_link = Mobile.objects.filter(Q(shop='Smartmobile'))
    link_kimovil_smartmobile  = []
    for i in mobile_link:
          link_kimovil_smartmobile.append(i.link.replace("https://smartmobile.cl/producto/" , "").partition("-global")[0])
    return (link_kimovil_smartmobile)

def DolarApi():
    try:
        response = requests.get('https://mindicador.cl/api')
        data = response.json()
        dolar = data['dolar']['valor']
        return dolar
    except:
        return "Murió Api"




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
           thumbnail = (item.find_all("img")[0]['src'])



           mobile = Mobile.objects.get_or_create(brand=brand, release_date="", price=price, model=model.lower(), screen_size=0, resolution="", dimensions="", weight=0, ram="",
                                          storage="",rear_camera="",front_camera="",score="",shop="Promovil",link=link , thumbnail = thumbnail)
    return render(request,'scraping.html')


def SmartmobileScraping(request):
    brands = ['xiaomi-smartphones', 'huawei', 'oneplus-smartphones']

    for brand in brands:
        website = "https://smartmobile.cl/categoria-producto/smartphones/brand"
        url = website.replace("brand", brand)
        source = requests.get(url)
        soup = BeautifulSoup(source.content, "lxml")

        summary = soup.find_all('main', {"class": "site-main"})
        if "-" in brand:
            brand = brand.split("-")[0]



        for item in summary:
            model = item.find_all("h2", {"class": "woocommerce-loop-product__title"})
            price = (item.find_all("span",{"class" : "electro-price"}))
            link = (item.find_all("div", {"class": "product-loop-header product-item__header"}))
            thumbnail = (item.find_all("img", {"class" : "attachment-woocommerce_thumbnail size-woocommerce_thumbnail"}))



            no_duplicates_list = list(dict.fromkeys(model))
            no_duplicates_price = list(dict.fromkeys(price))
            no_duplicates_link = list(dict.fromkeys(link))
            no_duplicates_thmbnail = list(dict.fromkeys(thumbnail))



            for i in range(len(no_duplicates_list)):
                model = (no_duplicates_list[i].text)
                if no_duplicates_price[i].find("ins"):
                    price = (no_duplicates_price[i].find("ins").text)
                else:
                    price = (no_duplicates_price[i].find("span", {"class": "woocommerce-Price-amount amount"}).text)

                link_bd =  link[i].find("a")['href']
                thumbnail_bd = no_duplicates_thmbnail[i]['src']

                mobile = Mobile.objects.get_or_create(brand=brand, release_date="", price=price, model=model.lower(), screen_size=0,
                                                    resolution="", dimensions="", weight=0, ram="",
                                                     storage="", rear_camera="", front_camera="", score="",
                                                      shop="Smartmobile", link=link_bd, thumbnail=thumbnail_bd)
    return render(request, 'scraping.html')


def checkScore():
    mobile_models = Mobile.objects.filter(Q(model__contains='one plus') | Q(model__contains='oneplus'))
    dict_scores = KimovilScraping()
   # for mobile in mobile_models:
       # print( mobile.model , [value for key, value in dict_scores.items() if mobile.model.find(key.lower()) != -1] )


def KimovilScraping():
    brands = ['oneplus']
    getLinkFromBD()
    score_dict = {}

    for brand in brands:
        for model in getLinkFromBD():
            model = model.lower()
            website = "https://www.kimovil.com/es/donde-comprar-model"
            url = website.replace("brand", brand)
            complete_url = url.replace("model",model)

            source = requests.get(complete_url)
            soup = BeautifulSoup(source.content, "lxml")

            summary = soup.find_all('div', {"class": "k-message opinions-score-message"})


            for item in summary:

                score = (item.find_all("div", {"class": "score"})[0].text)

               # price = (item.find_all("span", {"class": "price"})[0].text)
               # link = (item.find_all("a", {"class": "thumbnail product-thumbnail"})[0]['href'])
               # thumbnail = (item.find_all("img")[0]['src'])
                model = model.replace("-"," ").replace("/"," ")
                score = score.replace("\n","")
                score_dict.update({model: score})
                #print ({score: model})
                #if Mobile.objects.get(score="c"):
    return score_dict
                #mobile = Mobile.objects.filter(model__icontains=model).update(score=str(score))






def EbayApi(request):
    brands = ['Xiaomi', 'Huawei', 'OPPO' , 'OnePlus' ]

    for brand in brands:

        web_site = 'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=DiegoTar-TallerWe-PRD-ddfb0df12-769800d3&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&aspectFilter.aspectName=Network&aspectFilter.aspectValueName=Unlocked&aspectFilter.aspectName=Brand&aspectFilter.aspectValueName=phonebrand&itemFilter(0).name=Condition&itemFilter(0).value=New&itemFilter(1).name=FreeShippingOnly&itemFilter(1).value=true&itemFilter(2).name=HideDuplicateItems&itemFilter(2).value=true&categoryId=9355'
        url = web_site.replace("phonebrand", brand)

        Ebay_request = requests.get(url)
        product_data = Ebay_request.json()


        for i in range(100):

            model =  product_data['findItemsAdvancedResponse'][0]['searchResult'][0]['item'][i]['title'][0]
            price_usd =  product_data['findItemsAdvancedResponse'][0]['searchResult'][0]['item'][i]['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__']
            link = product_data['findItemsAdvancedResponse'][0]['searchResult'][0]['item'][i]['viewItemURL'][0]

            mobile = Mobile.objects.get_or_create(brand=brand, release_date="", price=price_usd, model=model.lower(), screen_size=0,
                                          resolution="", dimensions="", weight=0, ram="",
                                          storage="", rear_camera="", front_camera="", score="", shop="Ebay",
                                          link=link, thumbnail= "")


    return render(request, 'scraping.html')





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
