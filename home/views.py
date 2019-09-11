from django.http import HttpResponse
import requests
from django.shortcuts import render
from .models import Mobile
from bs4 import BeautifulSoup
from django.db.models import Q
from django.core.paginator import Paginator
from difflib import SequenceMatcher
from django.db.models import Count


all_models_sept_2019 = {
    'xiaomi' : ['redmi note 2', 'redmi note 2 prime', 'redmi 2 pro', 'redmi 2a prime', 'redmi note 3', 'redmi note 3 pro', 'redmi 3',
                'mi5', 'mi 5 pro', 'mi 5 high', 'redmi 3 pro', 'mi max', 'redmi 3s', 'redmi 3x', 'redmi pro', 'redmi 3s pro', 'redmi note 4', 'mi 5s',
                'mi 5s plus', 'mi max prime', 'mi note 2', 'mi mix', 'redmi 4 standard edition', 'redmi 4a' , 'redmi note 4',  'redmi note 4x', 'redmi 4x',
                'mi 5c', 'mi 6', 'mi max 2', 'redmi note 5', 'mi 5x', 'redmi note 5a', 'mi a1', 'mi mix 2', 'mi note 3', 'mi mix 2 special edition', 'redmi 5a',
                'redmi y1', 'redmo y1 lite', 'redmi 5', 'redmit 5 plus', 'redmi note 5 pro', 'mi mix 2s', 'mi 6x', 'black shark', 'redmi s2', 'mi 8', 'mi 8 se',
                'redmi y2', 'redmi 6', 'redmi 6a', 'redmi 6 pro', 'mi a2', 'mi a2 lite', 'mi max 3', 'pocophone f1', 'redmi note 6 pro','mi 8 pro', 'black shark 2',
                'mi mix 3', 'mi 8 lite', 'mi 9', 'mi 9 se', 'mi mix 3 5g','redmi 7', 'mi 9t' , 'mi 9t pro', 'mi a3', 'black shark 2 pro' ,'redmi note 7'] ,

    'oneplus' : ['3', '3t','5','5t','6','6t','7','7 pro', '7t'],
    'oppo' : ['reno a', 'a9 2020', 'reno2 z', 'reno2 f', 'r9s', 'reno z', 'reno ax5', 'r11 plus' , 'find x', 'r11s' , 'reno 10x', 'find 7', 'a77', 'rx17', 'r5'],
    'huawei' : ['nova 5i pro', 'mate 20 x 5g', 'nova 5', 'nova 5 pro', 'nova 5i', 'maimang 8', 'y9 prime', 'p30 lite','p smart z', 'y5 2019', 'p30', 'enjoy 9s'
                'enjoy 9e', 'p30 pro', 'mate 20', 'nova 4e', 'p smart+', 'y6 prime', 'mate x', 'y6 2019', 'y6 pro', 'nova lite 3', 'y7 prime', 'y7','y7 pro',
                'y max', 'y5 lite', 'mate 20 pro', 'mate 20 lite', 'p20', 'p20 lite', 'y7' , 'p10' , 'mate10']
}

prices_for_model = {}

def index(request):
    dolar = DolarApi()




    for brand in ['xiaomi','oneplus', 'huawei', 'oppo']:

        list_mobiles = getPriceByModel(request, brand, dolar)

        list_mobiles = { k : v for k,v in list_mobiles.items() if v}

        list_mobiles = tuple(list_mobiles.items())


        paginator = Paginator(list_mobiles, 6)

        page = request.GET.get('page')

        list_mobiles = paginator.get_page(page)



        context = {'valor_dolar': dolar, 'list_mobiles': list_mobiles, 'new_list_mobiles':prices_for_model}



    return render( request, 'search.html', context)

def afterExtractionOfData(request):


     writeAllExactModels('oneplus')
     writeAllExactModels('xiaomi')
     writeAllExactModels('huawei')
     writeAllExactModels('oppo')
     return render(request, 'scraping.html')



def productDetail(request, id):
    phone =  Mobile.objects.get(id=id)

    score = KimovilScraping(phone.exact_model)
    context = {'phone':phone, 'score':score}
    return  render(request, 'product_detail.html',context)

def getPriceByModel(request, brand, dolar):

    for model in all_models_sept_2019[brand]:
        prices_for_model.update({model: []})
        phones = Mobile.objects.filter(Q(exact_model=model)).values('id','model','shop','price','exact_model','link','thumbnail').annotate(total=Count('shop')).order_by('price')[:7]
        temp_shop = ['Ebay', 'Smartmobile', 'Promovil']

        query = request.GET.get('q')

        if query:
            phones = Mobile.objects.filter(Q(exact_model__icontains=query) | Q(brand__icontains=query) | Q(shop__icontains=query)).values('brand','id','model','shop','price','exact_model','link','thumbnail').annotate(total=Count('shop')).order_by('price')[:7]

        for phone in phones:
            #print (phone)

            if phone['exact_model'] == model and phone['shop'] in temp_shop :
                if phone['shop'] == "Ebay":
                    phone['price'] = '{:,.0f}'.format((int(phone['price'].split(".")[0]) * int(dolar))).replace(",",".")
                if len(prices_for_model[phone['exact_model']]) < 1:
                    prices_for_model[phone['exact_model']].append([phone['shop'], phone['price'], phone['link'],phone['id'],phone['model'][0:14], phone['thumbnail']])

                prices_for_model[phone['exact_model']].append([phone['shop'],phone['price'],phone['link']])
                temp_shop.remove(phone['shop'])


    return prices_for_model



def writeAllExactModels(brand):
    phones = Mobile.objects.filter((Q(shop="Promovil") | Q(shop="Smartmobile") | Q(shop="Ebay")) & (Q(brand=brand) | Q(brand=brand.capitalize()) | Q(brand=brand.upper())))



    for i in range(len(all_models_sept_2019[brand])):
        for phone in phones:
            if  brand + " " + all_models_sept_2019[brand][i] in phone.model.lower():
                phones.filter(id=phone.id).update(exact_model=all_models_sept_2019[brand][i])
    """
    for i in range(len(all_models_sept_2019['xiaomi'])):
        for phone in phones:
            if 'xiaomi' + " " + all_models_sept_2019['xiaomi'][i] in phone.model.lower():
                phones.filter(id=phone.id).update(exact_model=all_models_sept_2019['xiaomi'][i]) """
    """
    for i in range(len(all_models_sept_2019['huawei'])):
        for phone in phones:
            if 'huawei' + " " + all_models_sept_2019['huawei'][i] in phone.model.lower():
                phones.filter(id=phone.id).update(exact_model=all_models_sept_2019['huawei'][i])


    for next_phone in range(len(models)-1):
       if similar(models[next_phone], models[next_phone +1]) > 0.9:
           clean_models.append(models[next_phone])
       next_phone+=1
"""
    print("Marcas exactas escrita ")

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

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
    print ((set(all_oneplus_models)))
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
        response = requests.get('https://mindicador.cl/api')
        if response:
            data = response.json()
            dolar = data['dolar']['valor']
        else:
            dolar = 1

        return  dolar

def PromovilScraping(request):
    brands = ['40-oneplus', '69-huawei', '105-xiaomi']

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
                if len(price) > 10:
                    price = price.split(":")[1].replace(" ", "")

                mobile = Mobile.objects.get_or_create(brand=brand, release_date="", price=price, model=model.lower(), screen_size=0,
                                                    resolution="", dimensions="", weight=0, ram="",
                                                     storage="", rear_camera="", front_camera="", score="",
                                                      shop="Smartmobile", link=link_bd, thumbnail=thumbnail_bd)
    return render(request, 'scraping.html')

def KimovilScraping(exact_model):



    website = "https://www.kimovil.com/en/compare-smartphones/name.exact_model"
    url = website.replace("exact_model", exact_model)

    source = requests.get(url)
    soup = BeautifulSoup(source.content, "lxml")

    summary = soup.find_all('div', {"class": "objetive-wrap clear"})[0].text
    score = soup.find_all('div', {"class": "ki-rating"})[0].text
    screen_size =  soup.find('div', {"class": "data"})

    return score

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
            if 'galleryURL' in product_data['findItemsAdvancedResponse'][0]['searchResult'][0]['item'][i].keys():

                thumbnail = product_data['findItemsAdvancedResponse'][0]['searchResult'][0]['item'][i]['galleryURL'][0]
            print(model)
            print(thumbnail)
            mobile = Mobile.objects.get_or_create(brand=brand, release_date="", price=price_usd, model=model.lower(), screen_size=0,
                                          resolution="", dimensions="", weight=0, ram="",
                                          storage="", rear_camera="", front_camera="", score="", shop="Ebay",
                                          link=link, thumbnail= thumbnail)


    return render(request, 'scraping.html')





