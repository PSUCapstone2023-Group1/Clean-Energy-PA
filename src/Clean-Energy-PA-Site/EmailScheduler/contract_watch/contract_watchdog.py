from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from web_parser.papowerswitch_api import papowerswitch_api
from web_parser.responses.ratesearch import price_structure
import pandas as pd
from datetime import datetime, timedelta
from EmailScheduler.views import build_offer_path_less_than_rate
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance

api = papowerswitch_api()


class Contract_Watch_Dog:
    def __init__(self):
        self.subscribed_users_end_dates_df = pd.DataFrame()
        self.contract_end_dates_df = pd.DataFrame()
        self.lower_contract_options_df = pd.DataFrame()

    def get_susbscribers_contract_end_date(self):
        users = User.objects.all()
        subscribed_users_end_dates = []
        try:
            for user in users:
                user_preferences = User_Preferences.objects.get(
                    user_id=user, email_notifications=True
                )

                # Get the current end date and convert to usable format
                user_offer = user_preferences.get_selected_offer()
                # TODO: Last_Updated does not represent term_end_date
                # Need to add another attribute to user_pref for contract_end
                # And a means for user to update
                contract_end_date = self.convert_date_string_format(
                    user_offer.last_updated
                )

                subscribed_users_end_dates.append(
                    {
                        "email": user.email,
                        "zip_code": user_preferences.zip_code,
                        "distributor_id": user_preferences.distributor_id,
                        "rate_schedule": user_preferences.rate_schedule,
                        "contract_end_date": contract_end_date,
                        "selected_offer_rate": user_offer.rate,
                    }
                )

        except User_Preferences.DoesNotExist:
            pass
        # Create the subscribers DataFrame
        subscribed_users_end_dates_df = pd.DataFrame(subscribed_users_end_dates)
        return subscribed_users_end_dates_df

    def convert_date_string_format(self, date_string):
        contract_end_date = date_string
        input_date_format = "%B %d, %Y"
        converted_date_string = datetime.strptime(contract_end_date, input_date_format)
        return converted_date_string

    def calculate_days_left(self, df, date_column):
        current_date = datetime.now()
        df["days_left"] = df[date_column].apply(
            lambda date: (date - current_date).days
            if (date - current_date) > timedelta(days=0)
            else 0
        )
        return df

    def check_contract_end_dates_df(self):
        # Create a dataframe of subscriber emails and contract end dates
        subscribed_users_end_dates_df = self.get_susbscribers_contract_end_date()
        self.subscribed_users_end_dates_df = subscribed_users_end_dates_df

        # Add a column for days left on contract
        contract_end_dates_df = self.calculate_days_left(
            subscribed_users_end_dates_df, "contract_end_date"
        )

        lower_contract_options_df = pd.DataFrame()
        # For each subscriber, append lower rates/offers
        for index, row in contract_end_dates_df.iterrows():
            temp_lower_contract_options_df = (
                Price_Watch_Dog_Instance.build_lower_rate_mailing_list_df(row)
            )
            lower_contract_options_df = pd.concat(
                [lower_contract_options_df, temp_lower_contract_options_df],
                ignore_index=True,
            )

        lower_contract_options_df = lower_contract_options_df.dropna()
        # Set the class variable
        self.lower_contract_options_df = lower_contract_options_df
        self.contract_end_dates_df = contract_end_dates_df
        return contract_end_dates_df
