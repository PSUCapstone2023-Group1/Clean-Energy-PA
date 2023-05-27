from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class User_Preferences(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="default")
    zip_code = models.CharField(max_length=80, default="default")
    rate_schedule = models.CharField(max_length=80, default="default")
    distributor_id = models.CharField(max_length=80, default="default")
    selected_offer_id = models.CharField(max_length=80, default="default")

    def __str__(self):
        return self.rate_schedule
