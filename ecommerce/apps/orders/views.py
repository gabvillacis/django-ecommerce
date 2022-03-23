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
    get_object_or_404(Product, id=product_id)

    cart.add(product_id=product_id, qty=quantity)
    return JsonResponse({"added": True, "total_items": cart.__len__()})

def delete_from_cart(request):
    cart = Cart(request)    
    data = json.loads(request.body)
    product_id = int(data.get('product_id'))

    cart.delete(product_id=product_id)
    return JsonResponse({"deleted": True, "total_items": cart.__len__()})
        

def update_cart(request):
    pass