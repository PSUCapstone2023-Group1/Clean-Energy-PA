from django.db import models
from django.contrib.auth.models import User
from web_parser.responses.ratesearch import offer


# Create your models here.
class User_Preferences(models.Model):
    # Relationship to the user model
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="default")
    # The users zip code
    zip_code = models.CharField(max_length=10, default="default")
    # Distributor id from the api
    distributor_id = models.BigIntegerField(default=-1)
    # The rate schedule that the user saved
    rate_schedule = models.CharField(max_length=80, default="default")
    # Offer id from the api
    selected_offer = models.JSONField(default={})
    # Users email notification preference
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user_id)
    
    def get_selected_offer(self)->offer:
        return offer(self.selected_offer)
