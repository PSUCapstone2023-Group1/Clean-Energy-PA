from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class UserProfileChangeForm(UserChangeForm):
    # The users zip code
    zip_code = forms.CharField(max_length=10, required=False)
    # # Supplier
    # # TODO: Build this out
    # supplier = forms.CharField(max_length=80)
    # # Current Rate
    # # TODO: Build this out
    # current_rate = forms.CharField(max_length=80)
    # # Time left on contract
    # # TODO: Build this out
    # time_left_on_contract = forms.CharField(max_length=80)
    # Users email notification preference
    email_notifications = forms.BooleanField(
        initial=True, label="Enable Email Notifications", required=False
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "first_name",
            "last_name",
            "zip_code",
            # "supplier",
            # "current_rate",
            # "time_left_on_contract",
            "email_notifications",
        )
        # Excluding email and username, unless there is req. to have this...
        exclude = (
            "email",
            "username",
        )

    def __init__(self, *args, **kwargs):
        preference_instance = kwargs.pop("initial").get("preferences")
        initial = kwargs.get("initial", {})
        initial.update(
            {
                "zip_code": preference_instance.zip_code,
                "email_notifications": preference_instance.email_notifications,
            }
        )
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)
