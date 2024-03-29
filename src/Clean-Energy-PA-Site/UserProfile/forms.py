from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from datetime import date


class UserProfileChangeForm(UserChangeForm):
    # The users zip code
    zip_code = forms.CharField(max_length=10, required=False)
    # Users email notification preference
    email_notifications = forms.BooleanField(
        initial=True, label="Enable Email Notifications", required=False
    )
    # End date of the selected contract
    curr_year = date.today().year
    years = range(curr_year-2, curr_year+3)
    contract_end_date = forms.DateField(required=True, widget=forms.SelectDateWidget(years=years, months=None, empty_label="Set Contract End Date"))

    def clean(self):
        cleaned_data = super().clean()
        contract_end_date = cleaned_data.get("contract_end_date")
        if contract_end_date and contract_end_date < date.today():
            raise forms.ValidationError("Must pick a future date.")
        return cleaned_data
        
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
            "contract_end_date"
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
                "contract_end_date": preference_instance.selected_offer_expected_end
            }
        )
        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)
