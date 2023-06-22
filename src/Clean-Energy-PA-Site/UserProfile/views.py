from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from GreenEnergySearch.models import User_Preferences
from .forms import EmailNotificationPreferenceForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def sendDeleteConfirmationEmail(response, user, to_email):
    """Handles the logic for sending account deletion email to the user"""
    mail_subject = "Account Deletion: You're account has been deleted"
    message = render_to_string(
        "account_deletion_confirmation.html",
        {
            "user": user,
        },
    )

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        message = f"Dear <b>{user}</b>, please go to you email <b>{to_email}</b> to view you account deletion status <b>Note: </b>You may need to check your spam folder."
        success_message = f'<div class="alert alert-success">{message}</div>'
        messages.success(response, mark_safe(success_message))
    else:
        messages.error(
            response,
            f"Problem sending confirmation email to {to_email}, check if you typed it correctly.",
        )


@login_required
def profile(request):
    user_preferences = User_Preferences.objects.get(user_id=request.user)
    zip_code = user_preferences.zip_code

    user_profile = User_Preferences.objects.get(user_id=request.user)
    email_notifications = user_profile.email_notifications
    form = EmailNotificationPreferenceForm(
        initial={"email_notifications": email_notifications}
    )
    context = {"user": request.user, "zip_code": zip_code, "form": form}
    return render(request, "profile.html", context)


@login_required
def update_email_preferences(request):
    user_profile = User_Preferences.objects.get(user_id=request.user)
    if request.method == "POST":
        form = EmailNotificationPreferenceForm(request.POST)
        if form.is_valid():
            email_notifications = form.cleaned_data["email_notifications"]
            user_profile.email_notifications = email_notifications
            user_profile.save()
            return HttpResponseRedirect(f"{reverse('profile')}?form=success")
    else:
        email_notifications = user_profile.email_notifications
        form = EmailNotificationPreferenceForm(
            initial={"email_notifications": email_notifications}
        )

    context = {"form": form}
    return render(request, "profile.html", context)


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        # Get the email and first name prior to deleting...
        # ...the account to form the deletion email
        to_email = user.email
        username = user
        if user == request.user or user.is_superuser:
            # Delete the user account and associated data
            user.delete()
            sendDeleteConfirmationEmail(request, username, to_email)
            logout(request)
            return redirect("home")
    else:
        return render(request, "profile.html")


@login_required
def password_reset_from_profile(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been successfully updated.")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "password_reset_from_profile.html", {"form": form})
