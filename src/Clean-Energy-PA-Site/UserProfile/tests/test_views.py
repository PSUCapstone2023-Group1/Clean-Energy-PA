from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from GreenEnergySearch.models import User_Preferences


# Create your tests here.
class BaseTest(TestCase):
    """Base class for the view test cases"""

    def setUp(self):
        """Basic test setup, create a test user,
        set email notifications to True, log user in"""
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        User_Preferences.objects.create(user_id=self.user, email_notifications=True)
        self.profile_url = reverse("profile")
        self.client.login(username="testuser", password="testpassword")
        self.update_email_preferences_url = reverse("update_email_preferences")
        return super().setUp()


class UserProfileTest(BaseTest):
    def test_should_show_profile_page(self):
        """Test ID: Testing that the profile view can be loaded
        succesfully and the profile html template is being rendered"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_email_notification_preferences(self):
        """Test ID: Test verifies that the option for
        email_notification is available in the view"""
        response = self.client.get(self.profile_url)
        self.assertContains(response, "Email Notifications")
        self.assertContains(response, 'id="id_email_notifications"')
        self.assertContains(response, 'name="email_notifications"')
        self.assertContains(response, 'type="checkbox"')
        self.assertContains(response, "Save")

    def test_email_reminder_option_displayed(self):
        """Test ID: Verify that the email notification label
        is present in the HTML and that the checkbox element
        is present and accessible"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enable Email Notifications")
        checkbox = response.context["form"].fields["email_notifications"]

        self.assertIsNotNone(checkbox)
        self.assertEqual(checkbox.widget.input_type, "checkbox")

    def test_email_notification_initially_true_can_be_set_false(self):
        """Test ID: This test checks that the initial value of the checkbox is True,
        it then sets the value False and verifies it can be set False"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.initial["email_notifications"])
        # Update the email notification preference to False
        response = self.client.post(
            self.update_email_preferences_url, {"email_notifications": False}
        )
        updated_form = response.context["form"]
        updated_checkbox = updated_form["email_notifications"]
        self.assertFalse(updated_checkbox.value())


class UpdateEmailPreferencesTest(BaseTest):
    def test_non_post_method_to_update_email_preferences(self):
        """Test ID: Testing that non-POST branch of
        update_email_preferences view is reachable"""
        response = self.client.get(self.update_email_preferences_url)
        self.assertEqual(response.status_code, 200)
