from EmailScheduler.tests.test_price_watch_dog import PriceWatchDogTestCase
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance
from ..send_email_batch import email_batch
from unittest.mock import patch
import pandas as pd
from datetime import datetime, timedelta


class EmailBatchTestCase(PriceWatchDogTestCase):
    def setUp(self):
        super().setUp()

    def test_send_lower_rate_emails(self):
        email_batch_instance = email_batch.Email_Batch()
        email_batch_instance.send_lower_rate_emails()
        self.assertTrue(email_batch_instance.send_lower_rate_email_return)

    @patch("django.core.mail.send_mail")
    def test_send_lower_rate_emails_empty_dataframe(self, mock_send_mail):
        Price_Watch_Dog_Instance.subscribers_df = pd.DataFrame()
        Price_Watch_Dog_Instance.mailing_list_df = pd.DataFrame()

        email_batch_instance = email_batch.Email_Batch()
        email_batch_instance.send_lower_rate_emails()
        self.assertEqual(mock_send_mail.call_count, 0)
