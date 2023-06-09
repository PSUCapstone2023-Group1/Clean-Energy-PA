from django.urls import path, re_path, reverse
from . import views

app_name = "green_energy_search"

urlpatterns = [

     # ZipCode search from home
     re_path(r'^home/zipsearch/?$', views.zip_search,
               name="zip_search"),
     re_path(r'^home/zipsearch/rate_type/?$', 
          views.zip_search_distributor_selected, name="rate_type"),
     
     # Offer search
     path("distributor/<zipcode>/<distributor_id>/<rate_type>", 
          views.offer_search, name="offer_search")
]