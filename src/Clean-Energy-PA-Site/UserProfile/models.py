from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class User_Profile(models.Model):
    # Relationship to the user model
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default="default")
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return self.user_id.username
