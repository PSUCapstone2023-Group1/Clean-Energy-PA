from Website.tests.test_base import BaseTest
from EmailScheduler.send_email_batch import email_batch


class PriceWatchDogTestCase(BaseTest):
    def setUp(self):
        super().setUp()
        email_batch_instance = email_batch.Email_Batch()
