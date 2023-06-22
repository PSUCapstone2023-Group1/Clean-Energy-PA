from UserProfile.tests.test_user_profile_base_view import UserProfileBaseTest


class UpdateEmailPreferencesTest(UserProfileBaseTest):
    def test_non_post_method_to_update_email_preferences(self):
        """Test ID: Testing that non-POST branch of
        update_email_preferences view is reachable"""
        response = self.client.get(self.update_email_preferences_url)
        self.assertEqual(response.status_code, 200)
