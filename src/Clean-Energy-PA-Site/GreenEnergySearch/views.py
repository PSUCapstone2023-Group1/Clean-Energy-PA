from django.shortcuts import render


# Create your views here.
def home(response):
    return render(response, "GreenEnergySearch/home.html", {})
