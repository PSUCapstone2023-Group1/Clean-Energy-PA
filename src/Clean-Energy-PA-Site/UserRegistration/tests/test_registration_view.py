# future

# standard library

# third-party

# Django
from django.contrib.messages import get_messages

# local Django
from Website.tests.test_base import BaseTest
from UserRegistration.utils import generate_zip_code


class RegistrationViewTest(BaseTest):
    def _set_up_name_test(self, first_name, last_name, expected_status_code=None):
        """Helper function to set up first/last name form assignment"""
        self.form_data["first_name"] = first_name
        self.form_data["last_name"] = last_name
        response = self.client.post(self.register_url, self.form_data, follow=True)

        if expected_status_code is not None:
            self.assertEqual(response.status_code, expected_status_code)
        return response

    def test_registration_get_request(self):
        """
        Test ID 45: Registration page can be rendered with GET request
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration_redirect_to_login(self):
        """
        Test ID 8: Checking that valid form data will redirect to login
        """
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 302)
        expected_url = self.login_url
        self.assertRedirects(response, expected_url, fetch_redirect_response=False)

    def test_username_character_count_limit(self):
        """
        Test ID 12: Username field exceeding character limit will display error message
        """
        self.form_data["username"] = "a" * 151
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        expected_error_message = "Ensure this value has at most 150 characters"
        self.assertContains(response, expected_error_message)

    def test_zip_code_invalid_no_redirect(self):
        """
        Test ID 13: Checking that submitting invalid zip_code will not redirect
        """
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], self.register_url)

    def test_zip_code_invalid_error_message(self):
        """
        Test ID 15: Checking that invalid zip_code will display error message to user
        """
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid zip code.")

    def test_name_fields_not_empty(self):
        """
        Test ID 35: Checking that first_name and last_name will display error if empty
        """
        response = response = self._set_up_name_test("", "")
        self.assertFormError(response, "form", "first_name", "This field is required.")
        self.assertFormError(response, "form", "last_name", "This field is required.")

    def test_invalid_name_displays_error_message(self):
        """
        Test ID 38: Invalid name, exceeding 150 char will display error to user
        """
        invalid_name = "a" * 151
        response = self._set_up_name_test(invalid_name, invalid_name, 200)
        error_message = response.context["form"].errors
        self.assertIn("first_name", error_message)
        self.assertIn("last_name", error_message)
        self.assertEqual(
            error_message["first_name"],
            ["Ensure this value has at most 30 characters (it has 151)."],
        )
        self.assertEqual(
            error_message["last_name"],
            ["Ensure this value has at most 30 characters (it has 151)."],
        )
