from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile(response):
    return render(response, "profile.html", {})
