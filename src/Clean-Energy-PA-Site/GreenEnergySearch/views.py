from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from GreenEnergySearch.models import User_Preferences
from .forms import RegisterUser


# Create your views here.
def home(response):
    return render(response, "GreenEnergySearch/home.html", {})
