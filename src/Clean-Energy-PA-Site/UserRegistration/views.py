from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from GreenEnergySearch.models import User_Preferences
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import random

User = get_user_model()


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data["email"]
            username_base = email.split("@")[0]
            username = username_base
            while User.objects.filter(username=username).exists():
                username = f"{username_base}_{random.randint(1, 9999)}"

            user = User.objects.create(username=username)
            user.email = email
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.zip_code = form.cleaned_data["zip_code"]
            user.save()
            user_preferences = User_Preferences(
                user_id=user, zip_code=form.cleaned_data["zip_code"]
            )
            user_preferences.save()
            return redirect(reverse("login"))
    else:
        form = RegisterForm()
    return render(response, "UserRegistration/register.html", {"form": form})
