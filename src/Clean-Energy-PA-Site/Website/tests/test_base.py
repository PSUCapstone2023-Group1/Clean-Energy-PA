# future

# standard library

# third-party

# Django
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from GreenEnergySearch.models import User_Preferences
from web_parser.tests import ratesearch_test_data
from datetime import datetime

# local Django
from UserRegistration.utils import (
    generate_username,
    generate_email,
    generate_password,
    generate_name,
    generate_zip_code,
)

from UserRegistration.tokens import account_activation_token


class BaseTest(TestCase):
    """Base class for the view test cases"""

    def setUp(self):
        # UserRegistration Urls
        self.register_url = reverse("UserRegistration:register")
        self.login_url = reverse("UserRegistration:login")
        self.logout_url = reverse("UserRegistration:user_logout")

        # Dummy Form Data
        password = generate_password()
        self.form_data = {
            "username": generate_username(),
            "email": generate_email(),
            "first_name": generate_name(),
            "last_name": generate_name(),
            "zip_code": generate_zip_code(is_valid=True),
            "password1": password,
            "password2": password,
            "email_notifications": False,
        }

        # Create a new user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            is_active=False,
        )
        self.user.set_password("testpass")
        self.user.save()

        # Create a user preference base
        self.user_preferences = User_Preferences.objects.create(
            user_id=self.user,
            zip_code=15025,
            distributor_id=27498,
            rate_schedule="R - Regular Residential Service",
            selected_offer=ratesearch_test_data.expected_example[0],
            email_notifications=True
        )

        # Tokens used for email auth
        self.token = account_activation_token.make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        return super().setUp()

    def _login_user(self):
        # Make sure user is active
        form_data = {"username": "testuser", "password": "testpass"}
        url = reverse("UserRegistration:activate", kwargs={"uidb64": self.uid, "token": self.token})
        self.client.get(url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

        # Send post with valid form data to log user in
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(self.user.is_authenticated)
