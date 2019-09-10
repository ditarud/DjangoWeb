from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run/', views.PromovilScraping, name="PromovilScraping"),
    path('runEbay/', views.EbayApi , name="EbayApi"),
    path('runSm/', views.SmartmobileScraping, name="SmartmobileScraping"),
    path('product/<id>' , views.productDetail, name="productDetail"),
    path('create/' , views.afterExtractionOfData, name="afterExtractionOfData"),


]