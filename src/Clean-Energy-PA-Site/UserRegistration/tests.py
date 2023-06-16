from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from UserRegistration.utils import (
    generate_username,
    generate_email,
    generate_password,
    generate_name,
    generate_zip_code,
)


# Create your tests here.
class SignupLinkTest(TestCase):
    def test_signup_link_visible(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="btn btn-secondary" href="/register" role="button">Sign Up</a>',
        )


class RegistrationTest(TestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
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

    def _set_up_name_test(self, first_name, last_name, expected_status_code=None):
        self.form_data["first_name"] = first_name
        self.form_data["last_name"] = last_name
        response = self.client.post(self.register_url, self.form_data, follow=True)
        if expected_status_code is not None:
            self.assertEqual(response.status_code, expected_status_code)
        return response

    def _assert_not_in_database(
        self, response, existing_user_count, error_message=None
    ):
        self.assertEqual(response.status_code, 200)
        if error_message is not None:
            self.assertContains(response, error_message)
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count)

    def test_successful_registration_redirect_to_login(self):
        """Checking that valid form data will redirect to login"""
        # Simulate a POST request with valid registration data
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = self.login_url
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_successful_registration_creates_account(self):
        """Checking that valid form data will create user in database"""
        # Count the number of existing user accounts
        existing_user_count = User.objects.count()
        response = self.client.post(self.register_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count + 1)

    def test_unsuccessful_registration_no_account_created(self):
        """Checking that invalid form data will NOT create user in database"""
        # Count the number of existing user accounts
        existing_user_count = User.objects.count()
        self.form_data["email"] = "invalid email"
        response = self.client.post(self.register_url, self.form_data, follow=True)
        self._assert_not_in_database(response, existing_user_count)

    def test_registration_fails_if_account_exists(self):
        """Testing that no user is created in DB if one already exists"""
        # Create a user account with the same username as in the form data
        User.objects.create_user(
            username=self.form_data["username"], password="password123"
        )
        existing_user_count = User.objects.count()
        response = self.client.post(
            self.register_url, data=self.form_data, follow=False
        )
        error_message = "A user with that username already exists."
        self._assert_not_in_database(response, existing_user_count, error_message)

    def test_username_character_count_limit(self):
        # Modify the form_data to have a username with too many characters
        self.form_data["username"] = "a" * 151
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        expected_error_message = "Ensure this value has at most 150 characters"
        self.assertContains(response, expected_error_message)

    def test_zip_code_invalid_no_redirect(self):
        """Checking that submitting invalid zip_code will not redirect"""
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], self.register_url)

    def test_invalid_zip__no_account_created(self):
        """Checking that invalid zip_code will NOT create user in database"""
        existing_user_count = User.objects.count()
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data, follow=True)
        self._assert_not_in_database(response, existing_user_count)

    def test_zip_code_invalid_error_message(self):
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid zip code.")

    def test_name_fields_not_empty(self):
        response = response = self._set_up_name_test("", "")
        self.assertFormError(response, "form", "first_name", "This field is required.")
        self.assertFormError(response, "form", "last_name", "This field is required.")

    def test_name_saved_in_database(self):
        self._set_up_name_test("John", "Doe")
        saved_user = User.objects.get(first_name="John", last_name="Doe")
        self.assertEqual(saved_user.first_name, "John")
        self.assertEqual(saved_user.last_name, "Doe")

    def test_invalid_name_does_not_create_account(self):
        invalid_name = "a" * 151
        self._set_up_name_test(invalid_name, invalid_name, 200)
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_name_displays_error_message(self):
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

    def test_invalid_name_does_not_redirect_to_login(self):
        invalid_name = "a" * 151
        response = self._set_up_name_test(invalid_name, invalid_name, 200)
        self.assertTemplateUsed(response, "UserRegistration/register.html")
