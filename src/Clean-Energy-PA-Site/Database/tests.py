from django.test import TestCase
import models

# Hello World Model Test
class DjangoTest(TestCase):
    def create_user(self):
        self.user =  models.User(name="Billy Bob", zipcode=99999)

    def test_user_attribute(self):
        self.assertEqual(self.user.name, "Billy Bob")
        self.assertEqual(self.user.zipcode, 99999)
