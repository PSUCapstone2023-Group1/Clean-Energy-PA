from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User_Preferences(models.Model):
    # Relationship to the user model
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    # The users zip code
    zip_code = models.CharField(max_length=10, default="default")
    # The rate schedule that the user saved
    rate_schedule = models.CharField(max_length=80, default="default")
    # Distributor id from the api
    distributor_id = models.PositiveBigIntegerField(default=None)
    # Offer id from the api 
    selected_offer_id = models.PositiveBigIntegerField(default=None)
    # The price per kWh rate that the user saved
    selected_offer_rate = models.FloatField(default=None);

    def __str__(self):
        return self.rate_schedule
