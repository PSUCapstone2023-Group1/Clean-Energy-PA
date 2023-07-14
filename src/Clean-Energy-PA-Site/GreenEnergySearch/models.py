from django.db import models
from django.contrib.auth.models import User
from web_parser.responses.ratesearch import offer
from web_parser.responses.ratesearch import offer_collection


# Create your models here.
class User_Preferences(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="default")
    """Relationship to the user model"""
    zip_code = models.CharField(max_length=10, default="default")
    """The users zip code"""
    distributor_id = models.BigIntegerField(default=-1)
    """Distributor id from the api"""
    rate_schedule = models.CharField(max_length=80, default="default")
    """The rate schedule that the user saved"""
    selected_offer = models.JSONField(default=dict)
    """The offer that the user has selected"""
    possible_selections= models.JSONField(default=list[dict])
    """The possible selections that the user has chosen"""
    email_notifications = models.BooleanField(default=True)
    """Users email notification preference"""

    def __str__(self):
        return str(self.user_id)
    
    def get_selected_offer(self)->offer:
        return offer(self.selected_offer)
    
    def get_possible_selections(self)->offer_collection:
        return offer_collection(self.possible_selections)
