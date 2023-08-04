from Website.tests.test_base import BaseTest
from EmailScheduler.contract_watch.contract_watchdog_instance import (
    Contract_Watch_Dog_Instance,
)
import pandas as pd
import EmailScheduler.tests.data_for_test as data_for_test
from datetime import date, datetime


class ContractWatchDogTestCase(BaseTest):
    def setUp(self):
        # BaseTest setUp
        super().setUp()

        # Create a sample row Series
        self.valid_test_series = data_for_test.valid_test_series
        self.invalid_test_series = data_for_test.invalid_test_series

        # Sample Subscriber DF
        self.subscriber_df = pd.DataFrame(data_for_test.subscriber_data_list).astype(
            object
        )

        # Sample Lower Rates DF (mailing list)
        self.lower_rates_df = pd.DataFrame(data_for_test.lower_rates_data_list).astype(
            object
        )

        self.expected_data = data_for_test.expected_data

        self.contract_watch_dog_instance = Contract_Watch_Dog_Instance

    def test_get_susbscribers_contract_end_date(self):
        """
        Test ID 87: Verify that a subscribers data frame is returned 
        when get_subscribers_conrtact_end date is called
        """
        # Call the get_all_subscribers function
        test_subscribers_df = (
            self.contract_watch_dog_instance.get_susbscribers_contract_end_date()
        )

        expected_subscribed_users_end_dates_df = (
            data_for_test.expected_subscribed_users_end_dates_df
        )
        pd.testing.assert_frame_equal(
            test_subscribers_df, expected_subscribed_users_end_dates_df
        )
