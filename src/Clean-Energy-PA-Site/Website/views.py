from django.shortcuts import render
from django.http import HttpRequest
from GreenEnergySearch.models import User_Preferences

# Create your views here.
def home(request:HttpRequest):
    context = {}
    if request.user.is_authenticated:
        user_pref = User_Preferences.objects.get(user_id=request.user)
        context = {"user_pref":user_pref}
    return render(request, "base/home.html", context)

def base404(request, reason=None):
    return render(request, "base/404.html", {"reason":reason})