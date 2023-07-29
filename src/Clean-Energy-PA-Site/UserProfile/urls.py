from django.urls import path
from . import views

app_name = "user_profile"

urlpatterns = [
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("edit_profile/search_options", views.update_search_options, name="update_search_options"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path(
        "password_reset_from_profile/",
        views.password_reset_from_profile,
        name="password_reset_from_profile",
    ),
]
