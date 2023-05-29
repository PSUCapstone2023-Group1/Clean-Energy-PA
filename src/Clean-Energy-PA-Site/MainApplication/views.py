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


def view(response):
    return render(response, "MainApplication/view.html", {})
