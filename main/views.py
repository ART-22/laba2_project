from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Головна сторінка")

def about(request):
    return HttpResponse("Про нас")


