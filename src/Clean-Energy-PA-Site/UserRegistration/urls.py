from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "UserRegistration"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("registration/login/", views.user_login, name="login"),
    path("user_logout/", views.user_logout, name="user_logout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
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
    )
]
