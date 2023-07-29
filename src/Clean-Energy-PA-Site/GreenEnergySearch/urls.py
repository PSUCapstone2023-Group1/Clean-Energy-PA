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
     path("offersearch/<zipcode>/<distributor_id>/<rate_type>", 
          views.offer_search, name="offer_search"),

     path("user/preferences/possible_selections", views.possible_selections, name="possible_selections"),
     path("user/preferences/current_selection", views.current_selection, name="current_selection"), 
     path("user/preferences/search_options", views.search_options, name="search_options"), 
]