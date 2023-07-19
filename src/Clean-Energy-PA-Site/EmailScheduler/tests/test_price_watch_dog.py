from Website.tests.test_base import BaseTest
from EmailScheduler.price_watch.price_watchdog_instance import (
    Price_Watch_Dog_Instance,
)
from GreenEnergySearch.views import build_offer_path
from unittest.mock import patch
import pandas as pd


class PriceWatchDogTestCase(BaseTest):
    def setUp(self):
        # BaseTest setUp
        super().setUp()

        # Create a sample row Series
        input_row = {
            "email": "test@example.com",
            "zip_code": 15025,
            "rate_schedule": "RA - Residential Add - on Heat Pump Service",
            "distributor_id": 27487,
            "selected_offer_rate": 0.09,
        }

        self.test_series = pd.Series(input_row)

        self.subscriber_data_list = {
            "email": ["test@example.com"],
            "zip_code": ["15025"],
            "rate_schedule": ["R - Regular Residential Service"],
            "distributor_id": [27498],
            "selected_offer_rate": [0.0839],
        }
        self.subscriber_df = pd.DataFrame(self.subscriber_data_list).astype(object)

        t_email = "test@example.com"
        rate_type = "R - Regular Residential Service"
        dist_name = "PECO Energy"
        offer_path = build_offer_path(
            "15025", "27498", "R - Regular Residential Service"
        )
        self.lower_rates_data_list = {
            "email": [t_email, t_email, t_email],
            "zip_code": ["15025", "15025", "15025"],
            "rate_schedule": [rate_type, rate_type, rate_type],
            "distributor_id": [27498, 27498, 27498],
            "lower_distributor_id": [27498, 27498, 27498],
            "lower_distributor_name": [dist_name, dist_name, dist_name],
            "lower_offer_name": [
                "Achieve Energy Solutions LLC DBA EnergyPricing.com",
                "AEP Energy",
                "AP Gas & Electric (PA)",
            ],
            "lower_rate": [0.0709, 0.0755, 0.0755],
            "lower_rate_path": [offer_path, offer_path, offer_path],
        }

        self.lower_rates_df = pd.DataFrame(self.lower_rates_data_list).astype(object)

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
        series = self.test_series
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

    def test_build_lower_rate_mailing_list_df(self):
        # Create a sample row Series
        row = self.test_series

        # Call the build_lower_rate_mailing_list_df function
        result = self.price_watch_dog_instance.build_lower_rate_mailing_list_df(row)

        expected_data = {
            "email": ["test@example.com"],
            "zip_code": [15025],
            "rate_schedule": ["RA - Residential Add - on Heat Pump Service"],
            "distributor_id": [27487],
            "selected_offer_rate": [0.09],
            "lower_distributor_id": ["27487"],
            "lower_distributor_name": ["Duquesne Light"],
            "lower_offer_name": ["American Power & Gas of Pennsylvania LLC"],
            "lower_rate": [0.0899],
            "lower_rate_path": [
                build_offer_path(
                    "15025", 27487, "RA - Residential Add - on Heat Pump Service"
                ),
            ],
        }
        expected_result = pd.DataFrame(expected_data).astype(object)
        expected_result["lower_rate"] = expected_result["lower_rate"].astype(float)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_update_lower_rate_mailing_list_df(self):
        # Assert that the subscribers_df and mailing_list_df attributes have been updated correctly
        self.assertTrue(
            self.subscriber_df.equals(self.price_watch_dog_instance.subscribers_df)
        )
        self.assertTrue(
            self.lower_rates_df.equals(self.price_watch_dog_instance.mailing_list_df)
        )
