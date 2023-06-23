from django.urls import path
from . import views

app_name = "green_energy_search"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.home, name="home"),
]
