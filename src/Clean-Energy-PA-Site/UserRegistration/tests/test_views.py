# future

# standard library

# third-party

# Django
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

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
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        password = generate_password()
        self.form_data = {
            "username": generate_username(),
            "email": generate_email(),
            "first_name": generate_name(),
            "last_name": generate_name(),
            "zip_code": generate_zip_code(is_valid=True),
            "password1": password,
            "password2": password,
        }

        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass",
            is_active=False,
        )

        self.token = account_activation_token.make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        return super().setUp()

    def _set_up_name_test(self, first_name, last_name, expected_status_code=None):
        self.form_data["first_name"] = first_name
        self.form_data["last_name"] = last_name
        response = self.client.post(self.register_url, self.form_data, follow=True)

        if expected_status_code is not None:
            self.assertEqual(response.status_code, expected_status_code)
        return response


class HomeViewTest(BaseTest):
    def test_signup_link_visible(self):
        """
        Test ID 7: Verify that sign up link is visible.
        """
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="btn btn-secondary" href="/register" role="button">Sign Up</a>',
        )


class RegistrationViewTest(BaseTest):
    def test_registration_get_request(self):
        """
        Test ID: Registration page can be rendered with GET request
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration_redirect_to_login(self):
        """
        Test ID 8: Checking that valid form data will redirect to login
        """
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = self.login_url
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_username_character_count_limit(self):
        """
        Test ID 12: Username field exceeding character limit will display error message
        """
        self.form_data["username"] = "a" * 151
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        expected_error_message = "Ensure this value has at most 150 characters"
        self.assertContains(response, expected_error_message)

    def test_zip_code_invalid_no_redirect(self):
        """
        Test ID 13: Checking that submitting invalid zip_code will not redirect
        """
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], self.register_url)

    def test_zip_code_invalid_error_message(self):
        """
        Test ID 15: Checking that invalid zip_code will display error message to user
        """
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid zip code.")

    def test_name_fields_not_empty(self):
        """
        Test ID 35: Checking that first_name and last_name will display error if empty
        """
        response = response = self._set_up_name_test("", "")
        self.assertFormError(response, "form", "first_name", "This field is required.")
        self.assertFormError(response, "form", "last_name", "This field is required.")

    def test_invalid_name_displays_error_message(self):
        """
        Test ID 38: Invalid name, exceeding 150 char will display error to user
        """
        invalid_name = "a" * 151
        response = self._set_up_name_test(invalid_name, invalid_name, 200)
        error_message = response.context["form"].errors
        self.assertIn("first_name", error_message)
        self.assertIn("last_name", error_message)
        self.assertEqual(
            error_message["first_name"],
            ["Ensure this value has at most 30 characters (it has 151)."],
        )
        self.assertEqual(
            error_message["last_name"],
            ["Ensure this value has at most 30 characters (it has 151)."],
        )


class ActivateViewTest(BaseTest):
    def test_activate_valid_token(self):
        """Test ID: Valid token changes user.is_active to True"""
        url = reverse("activate", kwargs={"uidb64": self.uid, "token": self.token})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login"))
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Thank you for your email confirmation", str(messages))
        # Refresh the user from the database
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activate_invalid_token(self):
        """Test ID: Invalid token does not change user.is_active (default=False)"""
        # Change the token to an invalid one
        self.token = "invalid-token"
        url = reverse("activate", kwargs={"uidb64": self.uid, "token": self.token})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("login"))
        messages = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertIn("Activation link is invalid!", messages)
        # Refresh the user from the database
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_exception_path(self):
        """Test ID: Test covers the exception path of activate view"""
        url = reverse("activate", kwargs={"uidb64": "invalid", "token": "invalid"})
        self.client.get(url)
        self.assertRaises(Exception)


class LoginViewTest(BaseTest):
    def test_access_login(self):
        """Test ID: Test validates the login page is accessible"""
        # TODO: Figure out why user_login view isn't reporting as covered
        url = reverse("activate", kwargs={"uidb64": self.uid, "token": self.token})
        self.client.get(url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        login_successful = self.client.login(username="testuser", password="testpass")
        self.assertTrue(login_successful)
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(BaseTest):
    def test_access_logout(self):
        """Test ID: Test validates the logout page is accessible"""
        # TODO: Figure out why user_logout view isn't reporting as covered
        url = reverse("activate", kwargs={"uidb64": self.uid, "token": self.token})
        self.client.get(url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        login_successful = self.client.login(username="testuser", password="testpass")
        self.assertTrue(login_successful)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
