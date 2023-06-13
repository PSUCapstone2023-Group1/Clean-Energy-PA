from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import RegisterForm
from GreenEnergySearch.models import User_Preferences
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.utils.safestring import mark_safe

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token


def activate(response, uidb64, token):
    return redirect("login")


def activateEmail(response, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "UserRegistration/activate.html",
        {
            "user": user.username,
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


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.zip_code = form.cleaned_data["zip_code"]
            activateEmail(response, user, form.cleaned_data["email"])
            user.save()
            user_preferences = User_Preferences(
                user_id=user, zip_code=form.cleaned_data["zip_code"]
            )
            user_preferences.save()

            return redirect(reverse("login"))
    else:
        form = RegisterForm()
    return render(response, "UserRegistration/register.html", {"form": form})


def login(request):
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
