# future

# standard library

# third-party

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.safestring import mark_safe

# local Django
from GreenEnergySearch.models import User_Preferences
from .forms import UserProfileChangeForm


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
            return redirect(reverse("home"))
    else:
        return redirect(reverse("user_profile:edit_profile"))


@login_required
def password_reset_from_profile(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been successfully updated.")
            return redirect(reverse("user_profile:edit_profile"))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "password_reset_from_profile.html", {"form": form})


@login_required
def edit_profile(request):
    user = request.user
    try:
        user_preferences = User_Preferences.objects.get(user_id=user)
    except User_Preferences.DoesNotExist:
        user_preferences = None

    if request.method == "POST":
        form = UserProfileChangeForm(
            request.POST, instance=user, initial={"preferences": user_preferences}
        )
        if form.is_valid():
            # Update the user model
            user_instance = form.save(commit=False)
            user_instance.first_name = form.cleaned_data["first_name"]
            user_instance.last_name = form.cleaned_data["last_name"]
            user_instance.save()

            # Update the user_preferences
            if user_preferences:
                user_preferences.zip_code = form.cleaned_data["zip_code"]
                user_preferences.email_notifications = form.cleaned_data[
                    "email_notifications"
                ]
                user_preferences.save()
            else:
                user_preferences = User_Preferences(
                    user_id=user,
                    zip_code=form.cleaned_data["zip_code"],
                    email_notifications=form.cleaned_data["email_notifications"],
                )
                user_preferences.save()
    else:
        form = UserProfileChangeForm(
            instance=user, initial={"preferences": user_preferences}
        )

    context = {"user": request.user, "form": form}
    return render(request, "edit_profile.html", context)
