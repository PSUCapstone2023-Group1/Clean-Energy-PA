from GreenEnergySearch.views import build_offer_path
import pandas as pd
from datetime import datetime, timedelta

valid_input_row = {
    "email": "test@example.com",
    "zip_code": 19035,
    "rate_schedule": "R - Regular Residential Service",
    "distributor_id": 27498,
    "selected_offer_rate": 1.2,
}
valid_test_series = pd.Series(valid_input_row)

invalid_input_row = {
    "email": "test@example.com",
    "zip_code": 15025,
    "rate_schedule": "RA - Residential Add - on Heat Pump Service",
    "distributor_id": 27487,
    "selected_offer_rate": 0.09,
}
invalid_test_series = pd.Series(invalid_input_row)

subscriber_data_list = {
    "email": ["test@example.com"],
    "zip_code": ["15025"],
    "rate_schedule": ["R - Regular Residential Service"],
    "distributor_id": [27498],
    "selected_offer_rate": [0.0839],
}

t_email = "test@example.com"
rate_type = "R - Regular Residential Service"
dist_name = "PECO Energy"
offer_path = build_offer_path("15025", "27498", "R - Regular Residential Service")
lower_rates_data_list = {
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

expected_data = {
    "email": [],
    "zip_code": [],
    "rate_schedule": [],
    "distributor_id": [],
    "selected_offer_rate": [],
    "lower_distributor_id": [],
    "lower_distributor_name": [],
    "lower_offer_name": [],
    "lower_rate": [],
    "lower_rate_path": [],
}

empty_mailing_df = pd.DataFrame(expected_data)

current_date = datetime.now()
# Indexing book keeping input 31 days is really 30
thirty_days_left = current_date + timedelta(days=31)
expected_subscribed_users_end_dates_thirty_days = {
    "email": ["test@example.com"],
    "zip_code": ["15025"],
    "distributor_id": [27498],
    "rate_schedule": [rate_type],
    "contract_end_date": [f"{thirty_days_left}"],
    "selected_offer_rate": [0.0839],
}

expected_subscribed_users_end_dates = {
    "email": ["test@example.com"],
    "zip_code": ["15025"],
    "distributor_id": [27498],
    "rate_schedule": [rate_type],
    "contract_end_date": ["June 03, 2023"],
    "selected_offer_rate": [0.0839],
}


expected_subscribed_users_end_dates_df = pd.DataFrame(
    expected_subscribed_users_end_dates
)
