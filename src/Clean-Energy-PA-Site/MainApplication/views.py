from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from MainApplication.models import User_Preferences
from .forms import RegisterUser


# Create your views here.
def index(response, id):
    user = User_Preferences.objects.get(id=id)
    return render(response, "MainApplication/list.html", {"user": user})


def home(response):
    return render(response, "MainApplication/home.html", {})


def signup(response):
    if response.method == "POST":
        form = RegisterUser(response.POST or None)
        if form.is_valid():
            z = form.cleaned_data["zipcode"]
            rs = form.cleaned_data["rate_schedule"]
            d_id = form.cleaned_data["distributor_id"]
            so_id = form.cleaned_data["selected_offer_id"]
            up = User_Preferences(
                zipcode=z,
                rate_schedule=rs,
                distributor_id=d_id,
                selected_offer_id=so_id,
            )
            up.save()
            response.user.user_preferences_set.add(up)
        return HttpResponseRedirect("/%i" % up.id)
    else:
        form = RegisterUser()
    return render(response, "MainApplication/signup.html", {"form": form})


def view(response):
    return render(response, "MainApplication/view.html", {})
