# future

# standard library

# third-party

# Django

# local Django
from test_base import BaseTest
from django.urls import reverse

class HomeViewTest(BaseTest):
    def test_signup_link_visible(self):
        """
        Test ID 7: Verify that sign up link is visible.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="btn btn-secondary" href="/register" role="button">Sign Up</a>',
        )
