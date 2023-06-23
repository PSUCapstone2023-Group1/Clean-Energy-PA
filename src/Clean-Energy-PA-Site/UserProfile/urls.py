from django.urls import path
from . import views

app_name = "user_profile"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path(
        "update_email_preferences/",
        views.update_email_preferences,
        name="update_email_preferences",
    ),
    path("delete_account/", views.delete_account, name="delete_account"),
    path(
        "password_reset_from_profile/",
        views.password_reset_from_profile,
        name="password_reset_from_profile",
    ),
]
