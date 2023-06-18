from django.urls import path
from . import views

app_name = "UserProfile"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
]
