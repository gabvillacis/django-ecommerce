from django.shortcuts import render

from .models import Category, Product

def index(request):
    products = Product.objects.all()
    return render(request, "catalog/index.html", {'products': products})
