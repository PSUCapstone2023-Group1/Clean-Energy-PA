from test_base import BaseTest
from django.urls import reverse

class NotFoundViewTest(BaseTest):
    def test_404_page(self):
        """
        Test ID 67: Verify 404 view displays as expected.
        """
        response = self.client.get(reverse("notfound"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '404 - Not Found',
        )