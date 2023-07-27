# future

# standard library

# third-party

# Django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe

# local Django
from .forms import RegisterForm
from GreenEnergySearch.models import User_Preferences
from .tokens import account_activation_token


def activate_intermediary(request, uidb64, token):
    """Used as an intermediary view where user can
    press a button to activate their account"""
    uid = uidb64
    context = {"uid": uid, "token": token}
    return render(request, "activate_intermediary.html", context)


def activate(request):
    """Handles the logic once user clicks activation link from email"""
    if request.method == "POST":
        User = get_user_model()
        uidb64 = request.POST.get("uid")
        token = request.POST.get("token")
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            message = (
                "Thank you for your email confirmation. Now you can login your account."
            )
            success_message = f'<div class="alert alert-success">{message}</div>'
            messages.success(request, mark_safe(success_message))
            # messages.success(
            #     request,
            #     "Thank you for your email confirmation. Now you can login your account.",
            # )
            return redirect(reverse("UserRegistration:login"))
        else:
            message = "Activation link is invalid!"
            success_message = f'<div class="alert alert-danger">{message}</div>'
            messages.success(request, mark_safe(success_message))
            # messages.error(request, "Activation link is invalid!")
    else:
        return redirect(reverse("UserRegistration:activate"))
    return redirect(reverse("UserRegistration:login"))


def activateEmail(request, user, to_email):
    """Handles the logic for sending activation email to the user"""
    mail_subject = "Activate your user account."
    message = render_to_string(
        "activate.html",
        {
            "user": user,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        message = f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder."
        success_message = f'<div class="alert alert-success">{message}</div>'
        messages.success(request, mark_safe(success_message))
    else:
        messages.error(
            request,
            f"Problem sending confirmation email to {to_email}, check if you typed it correctly.",
        )


def register(request):
    """Logic for handling the user registration view"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Update default User model
            user = form.save(commit=False)
            email = request.POST.get("email")
            try:
                # Look for a user matching that email
                User = get_user_model()
                user = User.objects.get(email=email)
                messages.info(request, "An account with this email already exists!")
                return render(request, "register.html", {"form": form})
            except User.DoesNotExist:
                # If user with that email does not exist proceed
                user.is_active = False  # If user is NOT active they cannot log in
                user.username = form.cleaned_data["username"]
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.zip_code = form.cleaned_data["zip_code"]
                user.save()

                # Sends an email to the user to activate account
                activateEmail(request, user, form.cleaned_data["email"])

                # Update User_Preferences model
                user_preferences = User_Preferences(
                    user_id=user,
                    zip_code=form.cleaned_data["zip_code"],
                    email_notifications=form.cleaned_data["email_notifications"],
                )
                user_preferences.save()

                return redirect(reverse("UserRegistration:login"))
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


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
                return redirect(reverse("home"))
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
def user_logout(request):
    """Logic for handling the user logout view"""
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect(reverse("home"))
