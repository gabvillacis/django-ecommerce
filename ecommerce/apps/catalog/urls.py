from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.get_all_products, name="store_home"),
    path("categories/<slug:category_slug>/", views.get_all_products_by_category, name="store_category")
]