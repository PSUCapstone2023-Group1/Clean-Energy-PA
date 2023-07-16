from Website.tests.test_base import BaseTest
from django.urls import reverse

# Create your tests here.
class GreenEnergySearchBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()

        # urls
        green_energy_search_nmspce = "green_energy_search"
        self.zipsearch_name = f"{green_energy_search_nmspce}:zip_search"
        self.rate_type_name = f"{green_energy_search_nmspce}:rate_type"
        self.offersearch_name = f"{green_energy_search_nmspce}:offer_search"
        self.possible_selections_url = reverse(f"{green_energy_search_nmspce}:possible_selections")