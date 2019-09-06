from django.http import HttpResponse
import requests
from django.shortcuts import render
from .models import Mobile
from bs4 import BeautifulSoup


