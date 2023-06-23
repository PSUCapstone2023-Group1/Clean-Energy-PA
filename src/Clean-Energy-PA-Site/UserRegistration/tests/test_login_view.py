# future

# standard library

# third-party

# Django

# local Django
from UserRegistration.tests.test_base_view import BaseTest


class LoginViewTest(BaseTest):
    def test_access_login(self):
        """Test ID 42: Test validates the login page is accessible"""
        self._login_user()

    def test_get_login(self):
        """Test ID 43: Testing GET method to login page"""

        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
