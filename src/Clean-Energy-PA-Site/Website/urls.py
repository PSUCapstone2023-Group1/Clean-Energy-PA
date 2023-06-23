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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from UserRegistration.views import (
    register,
    user_login,
    user_logout,
    activate,
    # reset_password_from_login,
)
from UserProfile.views import (
    # profile,
    # update_email_preferences,
    delete_account,
    password_reset_from_profile,
    edit_profile,
)
from GreenEnergySearch.views import home


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    # GreenEnergySearch
    path("", include("GreenEnergySearch.urls")),
    path("home/", home, name="home"),
    # UserRegistration
    path("register/", register, name="register"),
    path("registration/login/", user_login, name="login"),
    path("user_logout/", user_logout, name="user_logout"),
    path("activate/<str:uidb64>/<str:token>/", activate, name="activate"),
    # UserRegistration: Password Reset [Logged out]
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/reset_password_from_login.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # UserProfile
    path("edit_profile/", edit_profile, name="edit_profile"),
    path("delete_account/", delete_account, name="delete_account"),
    path(
        "password_reset_from_profile/",
        password_reset_from_profile,
        name="password_reset_from_profile",
    ),
]
