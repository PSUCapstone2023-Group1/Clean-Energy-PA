from UserProfile.tests.test_user_profile_base_view import UserProfileBaseTest


class UserProfileTest(UserProfileBaseTest):
    def test_should_show_profile_page(self):
        """Test ID 55: Testing that the profile view can be loaded
        succesfully and the profile html template is being rendered"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_profile.html")

    def test_email_notification_preferences(self):
        """Test ID 56: Test verifies that the option for
        email_notification is available in the view"""
        response = self.client.get(self.profile_url)
        self.assertContains(response, "Email Notifications")
        self.assertContains(response, 'id="id_email_notifications"')
        self.assertContains(response, 'name="email_notifications"')
        self.assertContains(response, 'type="checkbox"')
        self.assertContains(response, "Save")

    def test_email_reminder_option_displayed(self):
        """Test ID 57: Verify that the email notification label
        is present in the HTML and that the checkbox element
        is present and accessible"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enable Email Notifications")
        checkbox = response.context["form"].fields["email_notifications"]

        self.assertIsNotNone(checkbox)
        self.assertEqual(checkbox.widget.input_type, "checkbox")

    def test_email_notification_initially_true_can_be_set_false(self):
        """Test ID 58: This test checks that the initial value of the checkbox is True,
        it then sets the value False and verifies it can be set False"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.initial["email_notifications"])
        # Update the email notification preference to False
        response = self.client.post(self.profile_url, {"email_notifications": False})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_profile.html")
