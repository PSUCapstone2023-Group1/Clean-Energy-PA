from django.shortcuts import render, redirect
from .forms import RegisterForm
from MainApplication.models import User_Preferences
from django.urls import reverse


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
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
