from django.test import TestCase
from django.urls import reverse
from django.shortcuts import resolve_url

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
                "password1": "password123",
                "password2": "password123",
            },
        )
        self.assertEqual(response.status_code, 302)
        # Check if the response redirects to the login page
        expected_url = reverse("login")
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)
