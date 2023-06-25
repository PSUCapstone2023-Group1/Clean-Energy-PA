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
        self.profile_url = reverse("edit_profile")
        self.account_deletion_url = reverse("delete_account")
        self.password_reset_from_profile_url = reverse("password_reset_from_profile")

        # Get the email notifications
        User_Preferences.objects.create(user_id=self.user, email_notifications=True)

        # Log user in, most of these tests user must already be logged in
        self._login_user()
