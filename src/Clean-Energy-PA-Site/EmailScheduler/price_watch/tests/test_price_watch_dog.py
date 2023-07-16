from Website.tests.test_base import BaseTest
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance
from GreenEnergySearch.views import build_offer_path
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

    def test_remove_rows_with_zero(self):
        price_watch_dog = Price_Watch_Dog_Instance
        # Create a sample DataFrame with a column containing zeros
        data = {"col1": [1, 2, 3, 0, 5]}
        df = pd.DataFrame(data)
        # Call the remove_rows_with_zero function
        result = price_watch_dog.remove_rows_with_zero(df, "col1")

        # Assert the expected output
        expected_data = {"col1": [1, 2, 3, 5]}
        expected_result = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_compare_rates(self):
        price_watch_dog = Price_Watch_Dog_Instance
        # Create a sample DataFrame with rate and lower_rate_threshold columns
        data = {"rate": [1, 2, 3, 4, 5], "lower_rate_threshold": [3, 3, 3, 3, 3]}
        df = pd.DataFrame(data)

        # Call the compare_rates function
        result = price_watch_dog.compare_rates(df, "rate", "lower_rate_threshold")

        # Assert the expected output
        expected_data = {"rate": [1, 2], "lower_rate_threshold": [3, 3]}
        expected_result = pd.DataFrame(expected_data)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_row_series_to_multiple_row_df(self):
        price_watch_dog = Price_Watch_Dog_Instance
        series = self.test_series
        # Call the row_series_to_multiple_row_df function with row_count = 3
        result = price_watch_dog.row_series_to_multiple_row_df(series, 3)
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
        price_watch_dog = Price_Watch_Dog_Instance

        # Call the get_all_subscribers function
        result = price_watch_dog.get_all_subscribers()

        expected_data = {
            "email": ["test@example.com"],
            "zip_code": ["15025"],
            "rate_schedule": ["R - Regular Residential Service"],
            "distributor_id": [27498],
            "selected_offer_rate": [0.0839],
        }
        expected_result = pd.DataFrame(expected_data).astype(object)
        expected_result["distributor_id"] = expected_result["distributor_id"].astype(
            "int64"
        )
        expected_result["selected_offer_rate"] = expected_result[
            "selected_offer_rate"
        ].astype(float)

        pd.testing.assert_frame_equal(result, expected_result)

    def test_build_lower_rate_mailing_list_df(self):
        price_watch_dog = Price_Watch_Dog_Instance

        # Create a sample row Series
        row = self.test_series

        # Call the build_lower_rate_mailing_list_df function
        result = price_watch_dog.build_lower_rate_mailing_list_df(row)

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
