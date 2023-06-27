from UserProfile.tests.test_user_profile_base_view import UserProfileBaseTest
from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


class UserProfileTest(UserProfileBaseTest):
    def test_edit_first_name(self):
        """Test ID 62: User should be able to modify their first name"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        # Retrieve the test user currently in the database
        first_name_in_database = User.objects.get(first_name=self.user.first_name)
        # Assert that the first_name is same as test user
        initial_first_name = response.context["form"]["first_name"].value()
        self.assertEqual(first_name_in_database.first_name, initial_first_name)
        # Send POST request to update first name
        response = self.client.post(reverse("edit_profile"), self.form_data)
        # Refresh the user and preferences from the database
        self.user.refresh_from_db()
        self.user_preferences.refresh_from_db()
        # Assert that the user model is updated with the new values
        self.assertEqual(self.user.first_name, self.form_data["first_name"])
        # Assert that the first_name is not equal to initial value
        self.assertNotEqual(self.user.first_name, initial_first_name)
        # Assert that the first name has changed in the view
        # GET request to reload the page
        response = self.client.get(reverse("edit_profile"))
        # Value of the first name in the form from view
        first_name_in_response = response.context["form"]["first_name"].value()
        # Assert that the value on the page is equal to what was submitted in the form
        self.assertEqual(first_name_in_response, self.form_data["first_name"])

    def test_edit_last_name(self):
        """Test ID 63: User should be able to modify their last name"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        # Retrieve the test user currently in the database
        last_name_in_database = User.objects.get(last_name=self.user.last_name)
        # Assert that the last_name is same as test user
        initial_last_name = response.context["form"]["last_name"].value()
        self.assertEqual(last_name_in_database.last_name, initial_last_name)
        # Send POST request to update last name
        response = self.client.post(reverse("edit_profile"), self.form_data)
        # Refresh the user and preferences from the database
        self.user.refresh_from_db()
        self.user_preferences.refresh_from_db()
        # Assert that the user model is updated with the new values
        self.assertEqual(self.user.last_name, self.form_data["last_name"])
        # Assert that the last_name is not equal to initial value
        self.assertNotEqual(self.user.last_name, initial_last_name)
        # Assert that the last name has changed in the view
        # GET request to reload the page
        response = self.client.get(reverse("edit_profile"))
        # Value of the last name in the form from view
        last_name_in_response = response.context["form"]["last_name"].value()
        # Assert that the value on the page is equal to what was submitted in the form
        self.assertEqual(last_name_in_response, self.form_data["last_name"])

    def test_edit_email_notifications(self):
        """Test ID 64: User should be able to modify their email notification preferences"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        # Retrieve the test users email notification preferences from db
        email_notificaitons_from_db = self.user_preferences.email_notifications
        # Assert that the email_notifications is same as test user
        initial_email_notifications = response.context["form"][
            "email_notifications"
        ].value()
        self.assertEqual(
            email_notificaitons_from_db,
            initial_email_notifications,
        )
        # Send POST request to update email_notifications name
        response = self.client.post(reverse("edit_profile"), self.form_data)
        # Refresh the user and preferences from the database
        self.user.refresh_from_db()
        self.user_preferences.refresh_from_db()
        # Assert that the user model is updated with the new values
        self.assertEqual(
            self.user_preferences.email_notifications,
            self.form_data["email_notifications"],
        )
        # Assert that the email_notifications is not equal to initial value
        self.assertNotEqual(
            self.user_preferences.email_notifications, initial_email_notifications
        )
        # Assert that the email_notifications name has changed in the view
        # GET request to reload the page
        response = self.client.get(reverse("edit_profile"))
        # Value of the email_notifications name in the form from view
        email_notifications_in_response = response.context["form"][
            "email_notifications"
        ].value()
        # Assert that the value on the page is equal to what was submitted in the form
        self.assertEqual(
            email_notifications_in_response,
            self.form_data["email_notifications"],
        )

    def test_edit_zip_code(self):
        """Test ID 65: User should be able to modify their zip_code"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        # Retrieve the test users zip code from db
        email_notificaitons_from_db = self.user_preferences.zip_code
        # Assert that the zip_code is same as test user
        initial_zip_code = int(response.context["form"]["zip_code"].value())
        self.assertEqual(
            email_notificaitons_from_db,
            initial_zip_code,
        )
        # Send POST request to update zip_code name
        response = self.client.post(reverse("edit_profile"), self.form_data)
        # Refresh the user and preferences from the database
        self.user.refresh_from_db()
        self.user_preferences.refresh_from_db()
        # Assert that the user model is updated with the new values
        self.assertEqual(
            self.user_preferences.zip_code,
            self.form_data["zip_code"],
        )
        # Assert that the zip_code is not equal to initial value
        self.assertNotEqual(self.user_preferences.zip_code, initial_zip_code)
        # Assert that the zip_code name has changed in the view
        # GET request to reload the page
        response = self.client.get(reverse("edit_profile"))
        # Value of the zip_code name in the form from view
        zip_code_in_response = response.context["form"]["zip_code"].value()
        # Assert that the value on the page is equal to what was submitted in the form
        self.assertEqual(
            zip_code_in_response,
            self.form_data["zip_code"],
        )
