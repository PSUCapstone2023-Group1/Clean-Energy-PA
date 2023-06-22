# future

# standard library

# third-party

# Django
from django.shortcuts import render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage

from django.template.loader import render_to_string

from django.urls import reverse

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe

# local Django
from .forms import RegisterForm
from GreenEnergySearch.models import User_Preferences
from .tokens import account_activation_token


def activate(response, uidb64, token):
    """Handles the logic once user clicks activation link from email"""
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            response,
            "Thank you for your email confirmation. Now you can login your account.",
        )
        return redirect("login")
    else:
        messages.error(response, "Activation link is invalid!")
    return redirect("login")


def activateEmail(response, user, to_email):
    """Handles the logic for sending activation email to the user"""
    mail_subject = "Activate your user account."
    message = render_to_string(
        "activate.html",
        {
            "user": user,
            "domain": get_current_site(response).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if response.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        message = f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder."
        success_message = f'<div class="alert alert-success">{message}</div>'
        messages.success(response, mark_safe(success_message))
    else:
        messages.error(
            response,
            f"Problem sending confirmation email to {to_email}, check if you typed it correctly.",
        )


def register(response):
    """Logic for handling the user registration view"""
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            # Update default User model
            user = form.save(commit=False)
            user.is_active = False  # If user is NOT active they cannot log in
            user.username = form.cleaned_data["username"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.zip_code = form.cleaned_data["zip_code"]
            user.save()

            # Sends an email to the user to activate account
            activateEmail(response, user, form.cleaned_data["email"])

            # Update User_Preferences model
            user_preferences = User_Preferences(
                user_id=user,
                zip_code=form.cleaned_data["zip_code"],
                email_notifications=form.cleaned_data["email_notifications"],
            )
            user_preferences.save()

            return redirect(reverse("login"))
    else:
        form = RegisterForm()
    return render(response, "register.html", {"form": form})


def user_login(request):
    """Logic for handling the user login view"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
def user_logout(response):
    """Logic for handling the user logout view"""
    logout(response)
    messages.info(response, "Logged out successfully!")
    return redirect("home")
