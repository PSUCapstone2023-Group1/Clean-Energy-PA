# future

# standard library

# third-party

# Django

# local Django
from UserRegistration.tests.test_base_view import BaseTest


class HomeViewTest(BaseTest):
    def test_signup_link_visible(self):
        """
        Test ID 7: Verify that sign up link is visible.
        """
        response = self.client.get("/home/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<a class="btn btn-secondary" href="/register" role="button">Sign Up</a>',
        )
