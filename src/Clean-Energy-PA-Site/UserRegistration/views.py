from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from GreenEnergySearch.models import User_Preferences
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


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
