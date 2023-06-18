from django.urls import path
from . import views

app_name = "UserProfile"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path(
        "update_email_preferences/",
        views.update_email_preferences,
        name="update_email_preferences",
    ),
]
