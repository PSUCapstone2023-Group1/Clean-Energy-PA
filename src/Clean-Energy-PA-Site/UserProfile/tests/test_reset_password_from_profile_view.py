from UserProfile.tests.test_user_profile_base_view import UserProfileBaseTest
from django.contrib.messages import get_messages
from django.urls import reverse


class ResetPasswordFromProfileTest(UserProfileBaseTest):
    def test_reset_password_from_profile(self):
        """Test ID 51: Testing that a user can reset their password from the profile page"""
        password_reset_form_data = {
            "old_password": "testpass",
            "new_password1": "updatedpassword",
            "new_password2": "updatedpassword",
        }
        response = self.client.post(
            self.password_reset_from_profile_url, password_reset_form_data
        )
        self.assertEqual(response.status_code, 302)

        # Make a request to log the user out
        response = self.client.get("/logout/")
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        form_data = {"username": "testuser", "password": "updatedpassword"}
        # Send post with valid form data to log user in
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(self.user.is_authenticated)

    def test_incorrect_old_password_displays_message(self):
        """Test ID 52: Testing that a user can reset their password from the profile page"""
        password_reset_form_data = {
            "old_password": "incorrect_old_pass",
            "new_password1": "updatedpassword",
            "new_password2": "updatedpassword",
        }
        response = self.client.post(
            self.password_reset_from_profile_url, password_reset_form_data
        )

        # Get the messages from the response
        messages = list(get_messages(response.wsgi_request))

        # Check if an error message is present
        self.assertTrue(
            any(
                "Please correct the errors below." in str(message)
                for message in messages
            )
        )

        # Make a request to log the user out
        response = self.client.get("/logout/")
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        form_data = {"username": "testuser", "password": "updatedpassword"}
        # Send post with invalid form data to log user in (but they should not be logged in)
        response = self.client.post(self.login_url, form_data)
        # No redirect
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_method_other_than_post_to_password_reset_from_profile_success(self):
        """Test ID 53: Testing that a method other than POST will be successful"""
        response = self.client.get(self.password_reset_from_profile_url)
        self.assertEqual(response.status_code, 200)
