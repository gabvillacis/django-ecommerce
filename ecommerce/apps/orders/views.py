from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from ecommerce.apps.catalog.models import Product
from .cart import Cart
import json

def get_cart_summary(request):
    cart = Cart(request)
    return render(request, "orders/cart.html", {"cart": cart})

def add_to_cart(request):    
    cart = Cart(request)

    data = json.loads(request.body)
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity'))
    product = get_object_or_404(Product, id=product_id)    
    cart.add(product=product, qty=quantity)

    return JsonResponse({"items": "hola123"})

def delete_from_cart(request):
    pass

def update_cart(request):
    pass