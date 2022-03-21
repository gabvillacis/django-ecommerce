from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def get_all_products(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "catalog/index.html", {"products": products})

def get_all_products_by_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=[category]
    )
    return render(request, "catalog/category.html", {"category": category, "products": products})
