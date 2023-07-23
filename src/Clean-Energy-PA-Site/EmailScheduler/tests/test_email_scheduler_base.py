from Website.tests.test_base import BaseTest
from unittest import mock

from web_parser.tests import zipsearch_test_data, ratesearch_test_data
from web_parser.responses.ratesearch import offer_collection
from web_parser.responses.zipsearch import distributor_collection


# Create your tests here.
class EmailSchedulerBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()

        # urls
        self.offersearch_name = "email_scheduler:offer_search_less_than_rate"
