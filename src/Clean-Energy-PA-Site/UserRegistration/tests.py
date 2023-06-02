from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url
from django.contrib.auth.models import User

from UserRegistration.utils import (
    generate_username,
    generate_email,
    generate_password,
    generate_name,
    generate_zip_code,
)


# Create your tests here.
# Test that Signup link is visible
class SignupLinkTest(TestCase):
    def test_signup_link_visible(self):
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)

        # Assert that the signup link is present in the rendered HTML
        self.assertContains(
            response, '<a class="nav-link" href="/register">Sign Up</a>'
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
            "zip_code": generate_zip_code(),
            "password1": password,
            "password2": password,
        }

    # Test that the user is re-directed to the login page
    def test_successful_registration_redirect_to_login(self):
        """Checking that valid form data will redirect to login"""
        # Simulate a POST request with valid registration data
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 302)
        # Check if the response redirects to the login page
        expected_url = self.login_url
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_successful_registration_creates_account(self):
        """Checking that valid form data will create user in database"""
        # Count the number of existing user accounts
        existing_user_count = User.objects.count()
        print(f"Existing User Count: {existing_user_count}")

        # Simulate a POST request with valid registration data
        response = self.client.post(self.register_url, self.form_data, follow=True)

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if a new user account is created
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count + 1)

    def test_unsuccessful_registration_no_account_created(self):
        """Checking that invalid form data will NOT create user in database"""
        # Count the number of existing user accounts
        existing_user_count = User.objects.count()
        print(f"Existing User Count: {existing_user_count}")

        # Simulate a POST request with invalid registration data
        self.form_data["email"] = "invalid email"
        response = self.client.post(self.register_url, self.form_data, follow=True)

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the number of user accounts remains the same
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count)

    def test_registration_fails_if_account_exists(self):
        """Testing that no user is created in DB if one already exists"""
        # Create a user account with the same username as in the form data
        User.objects.create_user(
            username=self.form_data["username"], password="password123"
        )
        existing_user_count = User.objects.count()
        # Simulate a POST request with the same registration data
        response = self.client.post(
            self.register_url, data=self.form_data, follow=False
        )

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains an error message
        self.assertContains(response, "A user with that username already exists.")

        # Check if no new user account is created
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count)

    def test_username_character_count_limit(self):
        # Modify the form_data to have a username with too many characters
        self.form_data["username"] = "a" * 151  # Assuming the character limit is 150

        # Submit the form and get the response
        response = self.client.post(self.register_url, self.form_data)

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the expected error message is present in the response content
        expected_error_message = "Ensure this value has at most 150 characters"
        self.assertContains(response, expected_error_message)
