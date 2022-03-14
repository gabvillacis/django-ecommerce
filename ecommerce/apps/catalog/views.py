from django.shortcuts import render

def index(request):
    render(request, "catalogue/index.html")
