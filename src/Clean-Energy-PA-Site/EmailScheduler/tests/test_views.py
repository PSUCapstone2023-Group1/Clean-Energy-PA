from .test_email_scheduler_base import EmailSchedulerBaseTest
from ..views import build_offer_path_less_than_rate, offer_search_less_than_rate
from bs4 import BeautifulSoup
from unittest import mock
from web_parser.tests import ratesearch_test_data
from web_parser.responses.ratesearch import offer_collection


class Email_Scheduler_View_Test(EmailSchedulerBaseTest):
    @mock.patch("web_parser.papowerswitch_api.get_offers")
    def test_offers_results(self, mock_get_offers):
        # Mock the distributors reponse
        mock_get_offers.return_value = offer_collection(
            ratesearch_test_data.expected_example
        )
        # self.mock_distributors_response(zipsearch_test_data.multiple_expected_example)

        # Create the zip_search url with a test zip code
        url = build_offer_path_less_than_rate(
            "15025", "27487", "RS%20-%20Regular%20Residential%20Service", "1.2"
        )

        # Generate reponse
        response = self.client.get(url)

        # Parse the response content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the element you want to test
        element = soup.find("div", id="offer-container")

        self.assertGreater(len(element.findChildren()), 0)

    def test_offers_no_distributor(self):
        url = build_offer_path_less_than_rate(
            "15025", None, "RS%20-%20Regular%20Residential%20Service", "1.2"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
