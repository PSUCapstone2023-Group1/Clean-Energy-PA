from Website.tests.test_base import BaseTest
from EmailScheduler.price_watch.price_watchdog_instance import (
    Price_Watch_Dog_Instance,
)
from GreenEnergySearch.views import build_offer_path
from unittest.mock import patch
import pandas as pd
import EmailScheduler.tests.data_for_test as data_for_test


class PriceWatchDogTestCase(BaseTest):
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

        self.price_watch_dog_instance = Price_Watch_Dog_Instance

        # Mock the get_all_subscribers method to return the subscribers_df
        with patch.object(
            self.price_watch_dog_instance,
            "get_all_subscribers",
            return_value=self.subscriber_df,
        ):
            # Mock the build_lower_rate_mailing_list_df method to return the lower_rates_df
            with patch.object(
                self.price_watch_dog_instance,
                "build_lower_rate_mailing_list_df",
                return_value=self.lower_rates_df,
            ):
                # Method under test
                self.price_watch_dog_instance.update_lower_rate_mailing_list_df()

    def test_remove_rows_with_zero(self):
        # Create a sample DataFrame with a column containing zeros
        data = {"col1": [1, 2, 3, 0, 5]}
        df = pd.DataFrame(data)
        # Call the remove_rows_with_zero function
        result = self.price_watch_dog_instance.remove_rows_with_zero(df, "col1")

        # Assert the expected output
        expected_data = {"col1": [1, 2, 3, 5]}
        expected_result = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_compare_rates(self):
        # price_watch_dog = Price_Watch_Dog_Instance
        # Create a sample DataFrame with rate and lower_rate_threshold columns
        data = {"rate": [1, 2, 3, 4, 5], "lower_rate_threshold": [3, 3, 3, 3, 3]}
        df = pd.DataFrame(data)

        # Call the compare_rates function
        result = self.price_watch_dog_instance.compare_rates(
            df, "rate", "lower_rate_threshold"
        )

        # Assert the expected output
        expected_data = {"rate": [1, 2], "lower_rate_threshold": [3, 3]}
        expected_result = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_row_series_to_multiple_row_df(self):
        series = self.invalid_test_series
        # Call the row_series_to_multiple_row_df function with row_count = 3
        result = self.price_watch_dog_instance.row_series_to_multiple_row_df(series, 3)
        e = "test@example.com"
        rs = "RA - Residential Add - on Heat Pump Service"
        # Assert the expected output
        expected_data = {
            "email": [e, e, e],
            "zip_code": [15025, 15025, 15025],
            "rate_schedule": [rs, rs, rs],
            "distributor_id": [27487, 27487, 27487],
            "selected_offer_rate": [0.09, 0.09, 0.09],
        }

        expected_result = pd.DataFrame(expected_data).astype(object)

        pd.testing.assert_frame_equal(result, expected_result)

    def test_get_all_subscribers(self):
        # Call the get_all_subscribers function
        test_subscribers_df = self.price_watch_dog_instance.get_all_subscribers()

        expected_subscribers_df = self.subscriber_df
        expected_subscribers_df["distributor_id"] = expected_subscribers_df[
            "distributor_id"
        ].astype("int64")
        expected_subscribers_df["selected_offer_rate"] = expected_subscribers_df[
            "selected_offer_rate"
        ].astype(float)

        pd.testing.assert_frame_equal(test_subscribers_df, expected_subscribers_df)

    def test_build_lower_rate_mailing_list_df_w_valid_series(self):
        # Create a sample row Series
        row = self.valid_test_series

        # Call the build_lower_rate_mailing_list_df function
        result = self.price_watch_dog_instance.build_lower_rate_mailing_list_df(row)

        # Assert there is data in the dataframe
        self.assertTrue(not result.empty)

    def test_build_lower_rate_mailing_list_df_w_invalid_series(self):
        # Create a sample row Series
        row = self.invalid_test_series

        # Call the build_lower_rate_mailing_list_df function
        result = self.price_watch_dog_instance.build_lower_rate_mailing_list_df(row)

        expected_data = self.expected_data
        expected_result = pd.DataFrame(expected_data).astype(object)
        pd.testing.assert_frame_equal(result, expected_result)
        self.assertTrue(result.empty)

    def test_update_lower_rate_mailing_list_df(self):
        # Assert that the subscribers_df and mailing_list_df attributes have been updated correctly
        self.assertTrue(
            self.subscriber_df.equals(self.price_watch_dog_instance.subscribers_df)
        )
        self.assertTrue(
            self.lower_rates_df.equals(self.price_watch_dog_instance.mailing_list_df)
        )
