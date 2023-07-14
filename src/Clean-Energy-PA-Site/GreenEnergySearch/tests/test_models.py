from .test_green_energy_base import GreenEnergySearchBaseTest
from GreenEnergySearch.models import User_Preferences
from django.contrib.auth.models import User
from web_parser.tests import ratesearch_test_data

class TestModels(GreenEnergySearchBaseTest):

    def setUp(self):
        super().setUp()

    def test_selected_offer(self):
        """Test ID TBD: Test verifies that the selected offer json works as expected"""
        self.assertEqual(self.user_preferences.get_selected_offer().id, str(ratesearch_test_data.expected_example[0]["id"]))
    
    def test_possible_selections(self):
        """Test ID TBD: Test verifies that the possible options is gettable"""
        self.assertEqual(len(self.user_preferences.get_possible_selections()), 2)