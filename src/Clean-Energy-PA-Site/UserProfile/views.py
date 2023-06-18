from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from GreenEnergySearch.models import User_Preferences
from .models import User_Profile
from .forms import EmailNotificationForm


@login_required
def profile(request):
    user_preferences = User_Preferences.objects.get(user_id=request.user)
    zip_code = user_preferences.zip_code

    user_profile = User_Profile.objects.get(user_id=request.user)
    email_notifications = user_profile.email_notifications
    form = EmailNotificationForm(initial={"email_notifications": email_notifications})
    context = {"user": request.user, "zip_code": zip_code, "form": form}
    return render(request, "profile.html", context)


@login_required
def update_email_preferences(request):
    user_profile = User_Profile.objects.get(user_id=request.user)
    if request.method == "POST":
        form = EmailNotificationForm(request.POST)
        if form.is_valid():
            email_notifications = form.cleaned_data["email_notifications"]
            user_profile.email_notifications = email_notifications
            user_profile.save()
            return redirect("profile")
    else:
        email_notifications = user_profile.email_notifications
        form = EmailNotificationForm(
            initial={"email_notifications": email_notifications}
        )

    context = {"form": form}
    return render(request, "profile.html", context)
