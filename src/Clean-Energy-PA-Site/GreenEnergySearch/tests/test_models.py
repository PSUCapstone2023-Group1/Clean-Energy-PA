from .test_green_energy_base import GreenEnergySearchBaseTest
from web_parser.tests import ratesearch_test_data
from web_parser.responses.ratesearch import offer

class TestModels(GreenEnergySearchBaseTest):

    def setUp(self):
        super().setUp()

    def test_selected_offer(self):
        """Test ID TBD: Test verifies that the selected offer json works as expected"""
        self.assertEqual(self.user_preferences.get_selected_offer().id, str(ratesearch_test_data.expected_example[0]["id"]))
    
    def test_possible_selections_build(self):
        """Test ID TBD: Test verifies that the possible options is gettable"""
        self.assertEqual(len(self.user_preferences.get_possible_selections()), 2)

    def test_add_possible_selections(self):
        """Test ID TBD: Test verifies that the possible options is gettable"""
        self.user_preferences.add_possible_selection(offer(ratesearch_test_data.expected_example[0]))
        self.assertEqual(len(self.user_preferences.get_possible_selections()), 3)

    def test_clear_possible_selections(self):
        """Test ID TBD: Test verifies that the possible options is gettable"""
        self.user_preferences.clear_possible_selections()
        self.assertEqual(len(self.user_preferences.get_possible_selections()), 0)