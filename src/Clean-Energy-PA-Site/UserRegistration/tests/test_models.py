# future

# standard library

# third-party

# Django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# local Django
from UserRegistration.utils import generate_zip_code

from UserRegistration.utils import (
    generate_username,
    generate_email,
    generate_password,
    generate_name,
    generate_zip_code,
)

class TestModels(TestCase):
    def setUp(self):
        self.register_url = reverse("UserRegistration:register")
        self.login_url = reverse("UserRegistration:login")
        password = generate_password()
        self.form_data = {
            "username": generate_username(),
            "email": generate_email(),
            "first_name": generate_name(),
            "last_name": generate_name(),
            "zip_code": generate_zip_code(is_valid=True),
            "password1": password,
            "password2": password,
        }

    def _set_up_name_test(self, first_name, last_name, expected_status_code=None):
        self.form_data["first_name"] = first_name
        self.form_data["last_name"] = last_name
        response = self.client.post(self.register_url, self.form_data, follow=True)
        if expected_status_code is not None:
            self.assertEqual(response.status_code, expected_status_code)
        return response

    def _assert_not_in_database(
        self, response, existing_user_count, error_message=None
    ):
        self.assertEqual(response.status_code, 200)
        if error_message is not None:
            self.assertContains(response, error_message)
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count)

    def test_successful_registration_creates_account(self):
        """
        Test ID 9: Checking that valid form data will create user in database
        """
        existing_user_count = User.objects.count()
        response = self.client.post(self.register_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_user_count = User.objects.count()
        self.assertEqual(new_user_count, existing_user_count + 1)

    def test_unsuccessful_registration_no_account_created(self):
        """
        Test ID 10: Checking that invalid form data will NOT create user in database
        """
        existing_user_count = User.objects.count()
        self.form_data["email"] = "invalid email"
        response = self.client.post(self.register_url, self.form_data, follow=True)
        self._assert_not_in_database(response, existing_user_count)

    def test_registration_fails_if_account_exists(self):
        """
        Test ID 11: Testing that no user is created in DB if one already exists
        """
        User.objects.create_user(
            username=self.form_data["username"], password="password123"
        )
        existing_user_count = User.objects.count()
        response = self.client.post(
            self.register_url, data=self.form_data, follow=False
        )
        error_message = "A user with that username already exists."
        self._assert_not_in_database(response, existing_user_count, error_message)

    def test_invalid_zip__no_account_created(self):
        """
        Test ID 14: Checking that invalid zip_code will NOT create user in database
        """
        existing_user_count = User.objects.count()
        self.form_data["zip_code"] = generate_zip_code(is_valid=False)
        response = self.client.post(self.register_url, self.form_data, follow=True)
        self._assert_not_in_database(response, existing_user_count)

    def test_name_saved_in_database(self):
        """
        Test ID 36: Checking that first_name and last_name can be saved in the database
        """
        self._set_up_name_test("John", "Doe")
        saved_user = User.objects.get(email="test@example.com")
        self.assertEqual(saved_user.first_name, "John")
        self.assertEqual(saved_user.last_name, "Doe")

    def test_invalid_name_does_not_create_account(self):
        """
        Test ID 37: Invalid name, exceeding 150 char
        cannot create an account
        """
        invalid_name = "a" * 151
        self._set_up_name_test(invalid_name, invalid_name, 200)
        # Setup adds a user to db so there should be 0 users in test db since this is an invalid name test
        self.assertEqual(User.objects.count(), 0)

    def test_user_with_email_already_exists(self):
        """
        Test ID 66: If a user enters an email that matches
        one already in the database they should not be
        allowed to create another account
        """
        self.form_data["email"] = "test@example.com"
        # Add the user with the test email
        self.client.post(self.register_url, self.form_data, follow=True)
        existing_user_count = User.objects.count()
        # Attempt to add the user again with the same email
        response = self.client.post(self.register_url, self.form_data, follow=True)
        new_user_count = User.objects.count()
        # Setup adds a user to db so there should be 1 user in test db
        self.assertEqual(existing_user_count, new_user_count)
        self.assertContains(response, "An account with this email already exists!")
