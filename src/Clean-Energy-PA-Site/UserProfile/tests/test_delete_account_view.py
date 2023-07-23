from django.urls import reverse
from django.contrib.auth.models import User
from UserProfile.tests.test_user_profile_base_view import UserProfileBaseTest
from UserProfile.views import sendDeleteConfirmationEmail
from unittest.mock import patch
from django.http import HttpRequest
from django.contrib.messages.api import MessageFailure


class DeleteAccountTest(UserProfileBaseTest):
    def test_account_deletion(self):
        """Test ID 49: Testing that the account deletion view can be loaded
        succesfully and the account_deletion html template is being rendered"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_profile.html")
        self.assertTrue(User.objects.filter(username="testuser").exists())
        # Simulate the user clicking "OK" on the confirmation popup
        response = self.client.post("/delete_account/", follow=True)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_non_post_method(self):
        """Test ID 50: Testing non-POST method"""
        response = self.client.get(self.account_deletion_url)
        self.assertEqual(response.status_code, 302)

    @patch("django.core.mail.EmailMessage.send")
    def test_send_delete_confirmation_email_failure(self, mock_send):
        # Set up a user and to_email for testing
        user = "TestUser"
        to_email = "test@example.com"

        mock_send.return_value = False

        # Call the sendDeleteConfirmationEmail function
        response = HttpRequest()
        with self.assertRaises(MessageFailure):
            sendDeleteConfirmationEmail(response, user, to_email)
