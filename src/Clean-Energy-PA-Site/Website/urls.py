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
from django.urls import include, path
from UserRegistration.views import register, user_login, user_logout, activate
from UserProfile.views import profile, update_email_preferences


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    # GreenEnergySearch
    path("", include("GreenEnergySearch.urls")),
    # UserRegistration
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("activate/<str:uidb64>/<str:token>/", activate, name="activate"),
    # UserProfile
    path("profile/", profile, name="profile"),
    path(
        "update_email_preferences/",
        update_email_preferences,
        name="update_email_preferences",
    ),
]
