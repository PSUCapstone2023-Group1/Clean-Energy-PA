from django.urls import reverse
from django.contrib.auth.models import User
from UserProfile.tests.test_user_profile_base_view import UserProfileBaseTest


class DeleteAccountTest(UserProfileBaseTest):
    def test_account_deletion(self):
        """Test ID 49: Testing that the account deletion view can be loaded
        succesfully and the account_deletion html template is being rendered"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertTrue(User.objects.filter(username="testuser").exists())
        # Simulate the user clicking "OK" on the confirmation popup
        response = self.client.post("/delete_account/", follow=True)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_non_post_method(self):
        """Test ID 50: Testing non-POST method"""
        response = self.client.get(self.account_deletion_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
