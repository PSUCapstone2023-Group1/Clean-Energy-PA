from Website.tests.test_base import BaseTest

# Create your tests here.
class EmailSchedulerBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()

        # urls
        self.offersearch_name = "email_scheduler:offer_search_less_than_rate"
