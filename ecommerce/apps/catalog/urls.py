from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.index, name="store_home")
]