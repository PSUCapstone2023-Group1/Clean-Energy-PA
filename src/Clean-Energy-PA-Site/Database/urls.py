from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("home/", views.home, name="home"),
    path("view/", views.view, name="view"),
]
