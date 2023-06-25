# future

# standard library

# third-party

# Django
from django.urls import reverse

# local Django
from UserRegistration.tests.test_base_view import BaseTest


class LogoutViewTest(BaseTest):
    def test_access_logout(self):
        """Test ID 44: Test validates the logout page is accessible"""
        self._login_user()
        response = self.client.get(reverse("user_logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)
