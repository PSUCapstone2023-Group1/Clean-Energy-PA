from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from uszipcode import SearchEngine

User = get_user_model()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    zip_code = forms.CharField(max_length=10)
    email_notifications = forms.BooleanField(
        required=False, initial=True, label="Receive Email Notifications"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "zip_code",
            "password1",
            "password2",
            "email_notifications",
        ]

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get("zip_code")

        # Perform validation and define custom error messages
        if not self.is_valid_zip_code(zip_code):
            raise forms.ValidationError("Invalid zip code.")

        return zip_code

    def is_valid_zip_code(self, zip_code):
        search = SearchEngine()
        result = search.by_zipcode(zip_code)
        return result is not None
