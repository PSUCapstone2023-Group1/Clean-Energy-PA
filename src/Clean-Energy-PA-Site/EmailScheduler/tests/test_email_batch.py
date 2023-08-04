from EmailScheduler.tests.test_price_watch_dog import PriceWatchDogTestCase
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance
from EmailScheduler.contract_watch.contract_watchdog_instance import (
    Contract_Watch_Dog_Instance,
)
from ..send_email_batch import email_batch
from unittest.mock import patch
import pandas as pd
from EmailScheduler.tests import data_for_test


class EmailBatchTestCase(PriceWatchDogTestCase):
    def setUp(self):
        super().setUp()

        self.subscribed_users_end_dates_df = pd.DataFrame(
            data_for_test.expected_subscribed_users_end_dates_thirty_days
        ).astype(object)

        self.subscribed_users_end_dates_df["contract_end_date"] = pd.to_datetime(
            self.subscribed_users_end_dates_df["contract_end_date"]
        ).dt.date

        self.contract_watch_dog_instance = Contract_Watch_Dog_Instance

        with patch.object(
            self.contract_watch_dog_instance,
            "get_susbscribers_contract_end_date",
            return_value=self.subscribed_users_end_dates_df,
        ):
            with patch.object(
                self.price_watch_dog_instance,
                "build_lower_rate_mailing_list_df",
                return_value=self.lower_rates_df,
            ):
                # Method under test
                self.contract_watch_dog_instance.check_contract_end_dates_df()

    def test_send_lower_rate_emails(self):
        """Test ID 80: Verify that an email will be sent to a 
        subscriber when there are rates lower than the subscribers selected rate
        """
        email_batch_instance = email_batch.Email_Batch()
        email_batch_instance.send_lower_rate_emails()
        self.assertTrue(email_batch_instance.send_lower_rate_email_return)

    def test_send_contract_expiration_emails_thirty_days(self):
        email_batch_instance = email_batch.Email_Batch()
        email_batch_instance.send_contract_expiration_emails()
        self.assertTrue(email_batch_instance.send_contract_end_email_return)

    @patch("django.core.mail.send_mail")
    def test_send_lower_rate_emails_empty_dataframe(self, mock_send_mail):
        """Test ID 81: Verify that an email will not be sent to a 
        subscriber when there are not rates lower than the subscribers selected rate
        """
        Price_Watch_Dog_Instance.subscribers_df = pd.DataFrame()
        Price_Watch_Dog_Instance.mailing_list_df = pd.DataFrame()

        email_batch_instance = email_batch.Email_Batch()
        email_batch_instance.send_lower_rate_emails()
        self.assertEqual(mock_send_mail.call_count, 0)
