from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "base/home.html", {})

def base404(request, reason=None):
    return render(request, "base/404.html", {"reason":reason})