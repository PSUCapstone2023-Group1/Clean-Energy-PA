from Website.tests.test_base import BaseTest
from django.urls import reverse
from web_parser.tests import ratesearch_test_data
from datetime import datetime

# Create your tests here.
class GreenEnergySearchBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()

        self.user_preferences.possible_selections= {"last_updated":str(datetime.now()),
                                "offers":[ratesearch_test_data.expected_example[0],
                                            ratesearch_test_data.expected_example[0]]}
        self.user_preferences.save()
        self.user_preferences.refresh_from_db()

        # urls
        green_energy_search_nmspce = "green_energy_search"
        self.zipsearch_name = f"{green_energy_search_nmspce}:zip_search"
        self.rate_type_name = f"{green_energy_search_nmspce}:rate_type"
        self.offersearch_name = f"{green_energy_search_nmspce}:offer_search"
        self.possible_selections_url = reverse(f"{green_energy_search_nmspce}:possible_selections")
        self.current_selection_url = reverse(f"{green_energy_search_nmspce}:current_selection")