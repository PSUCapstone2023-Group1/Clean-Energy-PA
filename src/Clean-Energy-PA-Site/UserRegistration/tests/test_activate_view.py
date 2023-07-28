# future

# standard library

# third-party

# Django
from django.contrib.messages import get_messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from ..tokens import account_activation_token

# local Django
from Website.tests.test_base import BaseTest


class ActivateViewTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activate_valid_token(self):
        """Test ID 46: Valid token changes user.is_active to True"""
        response = self.client.post(
            self.activate_url, {"uid": self.uidb64, "token": self.token}
        )
        self.assertRedirects(response, reverse("UserRegistration:login"))
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Thank you for your email confirmation", str(messages))
        # Refresh the user from the database
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_invalid_token(self):
        """Test ID 47: Invalid token does not change user.is_active (default=False)"""
        # Change the token to an invalid one
        self.token = "*************"
        response = self.client.post(
            self.activate_url, {"uid": self.uidb64, "token": self.token}
        )
        self.assertRedirects(response, reverse("UserRegistration:login"))
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Activation link is invalid!", messages)
        # Refresh the user from the database
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_exception_path(self):
        """Test ID 48: Test covers the exception path of activate view"""
        response = self.client.post(self.activate_url)
        self.assertRaises(Exception)

    def test_activate_exception_path(self):
        """Test ID TBD: Test covers the non-POST path"""
        response = self.client.get(self.activate_url)
        self.assertRedirects(response, reverse("UserRegistration:register"))
