from .test_green_energy_base import GreenEnergySearchBaseTest
from GreenEnergySearch.views import build_zip_search_path, build_rate_type_path, build_offer_path
from bs4 import BeautifulSoup
from unittest import mock
from web_parser.tests import zipsearch_test_data, ratesearch_test_data
from web_parser.responses.zipsearch import distributor_collection
from web_parser.responses.ratesearch import offer_collection

class Zip_Search_View_Test(GreenEnergySearchBaseTest):
    @mock.patch('web_parser.papowerswitch_api.papowerswitch_api.get_distributors')
    def test_distributors_selection(self, mock_get_distributors):
        """Test ID 59: Test verifies that the distributors are shown"""

        # Mock the distributors reponse
        mock_get_distributors.return_value = distributor_collection(zipsearch_test_data.multiple_expected_example)
        # self.mock_distributors_response(zipsearch_test_data.multiple_expected_example)

        # Create the zip_search url with a test zip code
        url = build_zip_search_path("15025")

        # Generate reponse
        response = self.client.get(url)

        # Parse the response content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element you want to test
        element = soup.find('div', id='distributor-container')

        self.assertEqual(len(element.findChildren()), 2)

    @mock.patch('web_parser.papowerswitch_api.papowerswitch_api.get_distributors')
    def test_rateschedule_selection(self, mock_get_distributors):
        """Test ID 60: Test verifies that the rate schedules are shown"""

        # Mock the distributors reponse
        mock_get_distributors.return_value = distributor_collection(zipsearch_test_data.multiple_expected_example)
        # self.mock_distributors_response(zipsearch_test_data.multiple_expected_example)

        # Create the zip_search url with a test zip code
        url = build_rate_type_path("15025", "27498")

        # Generate reponse
        response = self.client.get(url)

        # Parse the response content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element you want to test
        element = soup.find('div', id='rate-schedule-container')

        self.assertEqual(len(element.findChildren()), 2)
    
    @mock.patch('web_parser.papowerswitch_api.papowerswitch_api.get_offers')
    def test_offers_results(self, mock_get_offers):
        """Test ID 61: Test verifies that the offers are shown"""

        # Mock the distributors reponse
        mock_get_offers.return_value = offer_collection(ratesearch_test_data.expected_example)
        # self.mock_distributors_response(zipsearch_test_data.multiple_expected_example)

        # Create the zip_search url with a test zip code
        url = build_offer_path("15025", "27487", "RS%20-%20Regular%20Residential%20Service")

        # Generate reponse
        response = self.client.get(url)

        # Parse the response content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the element you want to test
        element = soup.find('div', id='offer-container')

        self.assertGreater(len(element.findChildren()), 0)