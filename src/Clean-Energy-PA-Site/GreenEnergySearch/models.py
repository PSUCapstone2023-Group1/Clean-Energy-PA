from django.db import models
from django.contrib.auth.models import User

from web_parser.responses.ratesearch import offer, offer_collection

from datetime import datetime
import json 

class possible_selections_obj:
    """The data model for the possible selections field"""
    def __init__(self):
        self.last_updated:datetime
        self.offers:offer_collection= offer_collection([])
    
    def add_offer(self, offer:offer):
        self.offers.collection.append(offer)

    def build(self, data):
        try:
            self.last_updated:datetime = datetime.fromisoformat(data["last_updated"])
            self.offers:offer_collection = offer_collection(data["offers"])
        except:
            return False

    def dump(self):
        return {"last_updated":str(self.last_updated), "offers":[json.loads(o.raw_json) for o in self.offers]}
    
    def __len__(self):
        return len(self.offers)

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
    possible_selections= models.JSONField(default={"last_updated":None, "offers":[]})
    """The possible selections that the user has chosen"""
    email_notifications = models.BooleanField(default=True)
    """Users email notification preference"""
    
    def __str__(self):
        return str(self.user_id)
    
    def get_selected_offer(self)->offer:
        return offer(self.selected_offer)
    
    def get_possible_selections(self)->possible_selections_obj:
        output = possible_selections_obj()
        output.build(self.possible_selections)
        return output

    def add_possible_selection(self, offer:offer):
        curr = self.get_possible_selections()
        curr.add_offer(offer)
        curr.last_updated = datetime.now()
        self.possible_selections = curr.dump()
        self.save()

    def clear_possible_selections(self):
        curr = self.get_possible_selections()
        curr.last_updated = datetime.now()
        curr.offers = []
        self.possible_selections = curr.dump()
        self.save()