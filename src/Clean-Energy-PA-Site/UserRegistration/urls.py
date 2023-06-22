from django.urls import path
from . import views

app_name = "UserRegistration"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("/registration/login/", views.user_login, name="login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
]
