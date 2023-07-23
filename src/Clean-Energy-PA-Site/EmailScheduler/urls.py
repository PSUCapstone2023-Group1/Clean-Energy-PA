from django.urls import path
from . import views

app_name = "email_scheduler"

# Offer search w/ Less Than Rate
urlpatterns = [
    path(
        "distributor/<zipcode>/<distributor_id>/<rate_type>/<less_than_rate>",
        views.offer_search_less_than_rate,
        name="offer_search_less_than_rate",
    )
]
