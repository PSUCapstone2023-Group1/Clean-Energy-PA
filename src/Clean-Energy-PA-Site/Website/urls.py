"""
URL configuration for Website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "base"

urlpatterns = [
    # Home
    path("", views.home, name="root"),
    path("home/", views.home, name="home"),

    #404
    path("404/", views.base404, name="notfound"),

    #Admin
    path("admin/", admin.site.urls),

    #Auth
    path("", include("django.contrib.auth.urls")),

    # GreenEnergySearch
    path("", include("GreenEnergySearch.urls")),

    # UserRegistration
    path("", include("UserRegistration.urls")),

    # UserProfile
    path("", include("UserProfile.urls")),
]
