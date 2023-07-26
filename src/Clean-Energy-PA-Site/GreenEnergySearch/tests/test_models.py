from .test_green_energy_base import GreenEnergySearchBaseTest
from web_parser.tests import ratesearch_test_data
from web_parser import offer
import copy

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
        
        #Create a "unique test entry to post"
        new_entry = copy.deepcopy(ratesearch_test_data.expected_example[0])
        new_entry["id"]=3

        self.user_preferences.add_possible_selection(offer(new_entry))
        self.assertEqual(len(self.user_preferences.get_possible_selections()), 3)

    def test_clear_possible_selections(self):
        """Test ID TBD: Test verifies that the possible options is gettable"""
        self.user_preferences.clear_possible_selections()
        self.assertEqual(len(self.user_preferences.get_possible_selections()), 0)