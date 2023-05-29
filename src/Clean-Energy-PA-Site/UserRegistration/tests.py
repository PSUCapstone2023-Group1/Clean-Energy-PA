from django.test import TestCase

# Create your tests here.


# Test that Signup link is visible
class SignupLinkTest(TestCase):
    def test_signup_link_visible(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

        # Assert that the signup link is present in the rendered HTML
        self.assertContains(response, '<a href="/register">Sign up</a>')
