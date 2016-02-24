from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("index page will go here")

def city(request):
    return HttpResponse("city view will go here")

def facility(request):
    return HttpResponse("facility detail page will go here")

def inspection_detail(request):
    return HttpResponse("inspection_detail will go here")

