from django.db import models
from django.contrib.auth.models import User

from web_parser.responses import offer, offer_collection

from datetime import date, datetime
import json 

class possible_selections_obj:
    """The data model for the possible selections field"""
    def __init__(self):
        self.last_updated:datetime
        self.offers:offer_collection= offer_collection([])
    
    def add_offer(self, offer:offer):
        for known_offer in self.offers.collection:
            if known_offer.equals(offer):
                return False
        self.offers.collection.append(offer)
        return True        

    def build(self, data):
        try:
            self.last_updated:datetime = datetime.fromisoformat(data["last_updated"])
            self.offers:offer_collection = offer_collection(data["offers"])
        except Exception:
            return False

    def dump(self):
        return {"last_updated":str(self.last_updated), "offers":[json.loads(o.raw_json) for o in self.offers]}
    
    def __len__(self):
        return len(self.offers)

# Create your models here.
class User_Preferences(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="default")
    """Relationship to the user model"""

    # Preferences
    email_notifications = models.BooleanField(default=True)
    """Users email notification preference"""

    # Search Options
    zip_code = models.CharField(max_length=10, default="default")
    """The users zip code"""
    distributor_id = models.BigIntegerField(default=-1)
    """Distributor id from the api"""
    distributor_name = models.CharField(max_length=80, default="")
    """The name of the distributor"""
    rate_schedule = models.CharField(max_length=80, default="default")
    """The rate schedule that the user saved"""

    # Current Contract Info
    selected_offer = models.JSONField(default=dict)
    """The offer that the user has selected"""
    selected_offer_selected_date = models.DateField(auto_now_add=True)
    """The date that the user selected the offer on our site"""
    selected_offer_expected_end = models.DateField(auto_now_add=True)
    """The expected end date of the offer based on when the user selected on our site"""

    # Storage for possible selections for the user
    possible_selections= models.JSONField(default={"last_updated":None, "offers":[]})
    """The possible selections that the user has chosen""" 
    
    def __str__(self):
        return str(self.user_id)
    
    def get_selected_offer(self)->offer:
        return offer(self.selected_offer)
    
    def get_possible_selections(self)->possible_selections_obj:
        output = possible_selections_obj()
        output.build(self.possible_selections)
        return output

    def get_selected_offer(self)->offer:
        return offer(self.selected_offer)

    def has_selected_offer(self)->bool:
        return len(self.selected_offer)>0

    def add_possible_selection(self, offer:offer):
        curr = self.get_possible_selections()
        if curr.add_offer(offer):
            curr.last_updated = datetime.now()
            self.possible_selections = curr.dump()
            self.save()
            return True
        return False

    def clear_possible_selections(self):
        curr = self.get_possible_selections()
        curr.last_updated = datetime.now()
        curr.offers = []
        self.possible_selections = curr.dump()
        self.save()