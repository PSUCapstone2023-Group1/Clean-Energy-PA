from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "UserRegistration"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("registration/login/", views.user_login, name="login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    # path(
    #     "reset_password_from_login/",
    #     views.reset_password_from_login,
    #     name="reset_password_from_login",
    # ),
    # Password reset URLs
]
