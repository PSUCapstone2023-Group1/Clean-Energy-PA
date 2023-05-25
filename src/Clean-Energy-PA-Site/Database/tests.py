from django.test import TestCase
from Database.models import User

# Hello World Model Test
class DjangoTest(TestCase):
    def create_user(self):
        self.user =  User(name="Billy Bob", zipcode=99999)

    def test_user_attribute(self):
        self.assertEqual(self.user.name, "Billy Bob")
        self.assertEqual(self.user.zipcode, 99999)
