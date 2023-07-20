from GreenEnergySearch.views import build_offer_path
import pandas as pd

input_row = {
    "email": "test@example.com",
    "zip_code": 15025,
    "rate_schedule": "RA - Residential Add - on Heat Pump Service",
    "distributor_id": 27487,
    "selected_offer_rate": 0.09,
}
test_series = pd.Series(input_row)

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
        build_offer_path("15025", 27487, "RA - Residential Add - on Heat Pump Service"),
    ],
}
