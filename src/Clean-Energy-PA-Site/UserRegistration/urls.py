from django.urls import path
from . import views

app_name = "UserRegistration"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
]
