from django.urls import reverse

from GreenEnergySearch.models import User_Preferences
from UserRegistration.tests.test_base_view import BaseTest


# Create your tests here.
class UserProfileBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()

        # setUp for UserProfileBaseTest

        # urls
        self.profile_url = reverse("profile")
        self.account_deletion_url = reverse("delete_account")
        self.update_email_preferences_url = reverse("update_email_preferences")

        # Get the email notifications
        User_Preferences.objects.create(user_id=self.user, email_notifications=True)

        # Log user in, most of these tests user must already be logged in
        self._login_user()
