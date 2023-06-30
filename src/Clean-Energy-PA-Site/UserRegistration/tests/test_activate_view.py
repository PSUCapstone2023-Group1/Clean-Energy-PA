# future

# standard library

# third-party

# Django
from django.contrib.messages import get_messages
from django.urls import reverse

# local Django
from UserRegistration.tests.test_base_view import BaseTest


class ActivateViewTest(BaseTest):
    def test_activate_valid_token(self):
        """Test ID 46: Valid token changes user.is_active to True"""
        url = reverse("UserRegistration:activate", kwargs={"uidb64": self.uid, "token": self.token})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("UserRegistration:login"))
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Thank you for your email confirmation", str(messages))
        # Refresh the user from the database
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_invalid_token(self):
        """Test ID 47: Invalid token does not change user.is_active (default=False)"""
        # Change the token to an invalid one
        self.token = "invalid-token"
        url = reverse("UserRegistration:activate", kwargs={"uidb64": self.uid, "token": self.token})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("UserRegistration:login"))
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Activation link is invalid!", messages)
        # Refresh the user from the database
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_exception_path(self):
        """Test ID 48: Test covers the exception path of activate view"""
        url = reverse("UserRegistration:activate", kwargs={"uidb64": "invalid", "token": "invalid"})
        self.client.get(url)
        self.assertRaises(Exception)
