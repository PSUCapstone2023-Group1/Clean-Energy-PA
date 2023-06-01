from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url
from django.contrib.auth.models import User
from UserRegistration.utils import generate_username, generate_email, generate_password


# Create your tests here.
# Test that Signup link is visible
class SignupLinkTest(TestCase):
    def test_signup_link_visible(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

        # Assert that the signup link is present in the rendered HTML
        self.assertContains(response, '<a href="/register">Sign up</a>')


# Test that the user is re-directed to the login page
class RegistrationTest(TestCase):
    def test_successful_registration_redirect_to_login(self):
        # Simulate a POST request with valid registration data
        response = self.client.post(
            reverse("register"),
            data={
                "username": "testuser",
                "email": "testuser@test.com",
                "password1": "password",
                "password2": "password",
            },
        )
        self.assertEqual(response.status_code, 302)
        # Check if the response redirects to the login page
        expected_url = reverse("login")
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_successful_registration_creates_account(self):
        # Count the number of existing user accounts
        existing_user_count = User.objects.count()
        print(f"Existing User Count: {existing_user_count}")

        # Generate a dummy password
        password = generate_password()

        # Simulate a POST request with valid registration data
        response = self.client.post(
            reverse("register"),
            data={
                "username": generate_username(),
                "email": generate_email(),
                "password1": password,
                "password2": password,
            },
            follow=True,
        )

        # Check if the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if a new user account is created
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count + 1)
