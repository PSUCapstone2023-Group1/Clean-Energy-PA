from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from web_parser.papowerswitch_api import papowerswitch_api
import pandas as pd

api = papowerswitch_api()


class Price_Watch_Dog:
    def remove_rows_with_zero(self, df, col):
        """Keep rates that are not zero"""
        df = df[df[col] != 0]
        return df

    def compare_rates(self, df, rate, lower_rate_threshold):
        """Keep rates that are lower than threshold"""
        df = df[df[rate] < df[lower_rate_threshold]]
        return df

    def get_all_subscribers(self):
        """Returns a dataframe of all subscribers
        (folks who selected True for email notifications)"""
        users = User.objects.all()
        subscribed_users = []
        for user in users:
            try:
                user_preferences = User_Preferences.objects.get(
                    user_id=user, email_notifications=True
                )

                user_offer = user_preferences.get_selected_offer()
                # Create a list that will be converted to pandas DataFrame
                subscribed_users.append(
                    {
                        "email": user.email,
                        "zip_code": user_preferences.zip_code,
                        "rate_schedule": user_preferences.rate_schedule,
                        "distributor_id": user_preferences.distributor_id,
                        "selected_offer_rate": user_offer.rate,
                    }
                )
            except User_Preferences.DoesNotExist:
                pass
        # Create the subscribers DataFrame
        subscribers_df = pd.DataFrame(subscribed_users)
        return subscribers_df

    def build_lower_rate_mailing_list_df(self, row):
        # Zip Search on subcriber zip_code row
        distributors = api.get_distributors(row["zip_code"])
        # Temp list to hold appended data
        data = []
        # Get offers for each distributor and build the mailing list
        for distributor in distributors:
            # Rate Search on all available distributors
            # **assuming subscribers existing rate_schedule**
            offers = api.get_offers(distributor.id, row["rate_schedule"])
            for offer in offers:
                rate = offer.rate
                # Build out the mailing list that will be converted to dataframe
                data.append(
                    {
                        # Subscriber data (user data from db w/ email_notification=True)
                        "email": row["email"],
                        "zip_code": row["zip_code"],
                        "rate_schedule": row["rate_schedule"],
                        "existing_distributor_id": row["distributor_id"],
                        "existing_offer_rate": row["selected_offer_rate"],
                        # Returned from the Rate Search, lower rate data
                        "lower_distributor_id": distributor.id,
                        "lower_distributor_name": distributor.name,
                        "lower_offer_name": offer.name,
                        "lower_rate": rate,
                    }
                )
        # Create the mailing_list DataFrame
        lower_rate_mailing_list_df = pd.DataFrame(data)

        # If Rate Search returns a rate of 0 remove row
        lower_rate_mailing_list_df = self.remove_rows_with_zero(
            lower_rate_mailing_list_df, "lower_rate"
        )

        # Remove any duplicates
        lower_rate_mailing_list_df = lower_rate_mailing_list_df.drop_duplicates()

        # Compare rates and only keep rates that are lower than users existing (threshold)
        lower_rate_mailing_list_df = self.compare_rates(
            lower_rate_mailing_list_df, "lower_rate", "existing_offer_rate"
        )
        return lower_rate_mailing_list_df

    def check_user_rates(self):
        subscribers_df = self.get_all_subscribers()
        lower_rate_mailing_list_df = pd.DataFrame()  # Create an empty DataFrame

        # For each subscriber, append lower rates/offers
        for index, row in subscribers_df.iterrows():
            lower_rates_df = self.build_lower_rate_mailing_list_df(row)
            lower_rate_mailing_list_df = pd.concat(
                [lower_rate_mailing_list_df, lower_rates_df], ignore_index=True
            )
