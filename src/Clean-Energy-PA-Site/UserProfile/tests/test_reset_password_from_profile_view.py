from UserProfile.tests.test_user_profile_base_view import UserProfileBaseTest
from django.contrib.messages import get_messages


class ResetPasswordFromProfileTest(UserProfileBaseTest):
    def test_reset_password_from_profile(self):
        password_reset_form_data = {
            "old_password": "testpass",
            "new_password1": "updatedpassword",
            "new_password2": "updatedpassword",
        }
        response = self.client.post(
            self.password_reset_from_profile_url, password_reset_form_data
        )
        self.assertEqual(response.status_code, 302)

    def test_incorrect_old_password_displays_message(self):
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

    def test_method_other_than_post_to_password_reset_from_profile_success(self):
        """Test ID: Testing that a method other than POST will be successful"""
        response = self.client.get(self.password_reset_from_profile_url)
        self.assertEqual(response.status_code, 200)
