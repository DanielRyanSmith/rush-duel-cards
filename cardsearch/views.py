from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Card search view.")

def search(request):
    return HttpResponse("search results.")

def advanced(request):
    return HttpResponse("advanced search.")