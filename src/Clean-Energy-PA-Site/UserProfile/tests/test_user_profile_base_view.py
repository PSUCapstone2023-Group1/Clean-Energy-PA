from django.urls import reverse

from GreenEnergySearch.models import User_Preferences
from Website.tests.test_base import BaseTest


# Create your tests here.
class UserProfileBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()

        # setUp for UserProfileBaseTest

        # urls
        self.profile_url = reverse("user_profile:edit_profile")
        self.account_deletion_url = reverse("user_profile:delete_account")
        self.password_reset_from_profile_url = reverse("user_profile:password_reset_from_profile")

        # Get the email notifications
        self.user_preferences = User_Preferences.objects.create(
            user_id=self.user, email_notifications=True, zip_code=15025
        )

        # Log user in, most of these tests user must already be logged in
        self._login_user()
