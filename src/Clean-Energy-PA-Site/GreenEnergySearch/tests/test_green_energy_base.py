from Website.tests.test_base import BaseTest
from unittest import mock

from web_parser.tests import zipsearch_test_data, ratesearch_test_data
from web_parser.responses.ratesearch import offer_collection
from web_parser.responses.zipsearch import distributor_collection

# Create your tests here.
class GreenEnergySearchBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()

        # urls
        self.zipsearch_name = "green_energy_search:zip_search"
        self.rate_type_name = "green_energy_search:rate_type"
        self.offersearch_name = "green_energy_search:offer_search"