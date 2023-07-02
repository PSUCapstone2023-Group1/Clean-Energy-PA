from Website.tests.test_base import BaseTest
from unittest import mock

from web_parser.tests import zipsearch_test_data, ratesearch_test_data
from web_parser.responses.ratesearch import offer_collection
from web_parser.responses.zipsearch import distributor_collection


# Create your tests here.
class GreenEnergySearchBaseTest(BaseTest):
    @mock.patch('web_parser.papowerswitch_api.papowerswitch_api')
    def setUp(self, mock_web_parser:mock.Mock):
        # Setup the BaseTest first
        super().setUp()
        
        # urls
        self.zipsearch_name = "green_energy_search:zip_search"
        self.rate_type_name = "green_energy_search:rate_type"
        self.offersearch_name = "green_energy_search:offer_search"

        # Mock web_parser
        self.mock_web_parser = mock_web_parser

        # Default distributor mock
        self.mock_distributors_response(zipsearch_test_data.expected_example)

        # Default offers mock
        self.mock_offers_response(ratesearch_test_data.expected_example)

    def mock_distributors_response(self, test_data):
        self.mock_web_parser.return_value.get_distributors.return_value = distributor_collection(test_data)
    
    def mock_offers_response(self, test_data):
        self.mock_web_parser.return_value.get_offers.return_value =  offer_collection(test_data)