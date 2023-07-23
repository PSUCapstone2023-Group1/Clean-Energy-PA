from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from EmailScheduler.views import build_offer_path_less_than_rate
from django.urls import reverse
from web_parser.papowerswitch_api import papowerswitch_api
from web_parser.responses.ratesearch import price_structure
import pandas as pd

api = papowerswitch_api()


class Price_Watch_Dog:
    def __init__(self):
        self.subscribers_df = pd.DataFrame()
        self.mailing_list_df = pd.DataFrame()

    def remove_rows_with_zero(self, df, col):
        """Keep rates that are not zero"""
        df = df[df[col] != 0]
        df.reset_index(drop=True, inplace=True)
        return df

    def compare_rates(self, df, rate, lower_rate_threshold):
        """Keep rates that are lower than threshold"""
        df = df[df[rate] < df[lower_rate_threshold]]
        df.reset_index(drop=True, inplace=True)
        return df

    def row_series_to_multiple_row_df(self, row, row_count):
        """Converts a row Series to a DataFrame
        with repeated # row_count rows"""
        df = row.to_frame()  # row Series to DataFrame
        df = df.transpose()
        # Repeat rows to match specified row_count
        df = pd.concat([df] * row_count, ignore_index=True)
        # df.reset_index(drop=True, inplace=True)
        return df

    def get_all_subscribers(self):
        """Returns a dataframe of all subscribers
        (folks who selected True for email notifications)"""
        users = User.objects.all()
        subscribed_users = []
        for user in users:
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
        # Create the subscribers DataFrame
        subscribers_df = pd.DataFrame(subscribed_users)
        return subscribers_df

    def get_lower_rate_filtered_offers(self, offers, rate):
        def sorter(val):
            return val.rate

        filtered_offers = offers.filter(
            renewable_energy=True,
            price_structure=price_structure.fixed,
            upper_rate=float(rate),
        )
        filtered_offers.sort(key=sorter)
        return filtered_offers

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

            # Return only offers less than users selected offer
            filtered_offers = self.get_lower_rate_filtered_offers(
                offers, row["selected_offer_rate"]
            )

            for offer in filtered_offers:
                rate = offer.rate
                # Build out the mailing list that will be converted to dataframe
                data.append(
                    {
                        # Returned from the Rate Search, lower rate data
                        "lower_distributor_id": distributor.id,
                        "lower_distributor_name": distributor.name,
                        "lower_offer_name": offer.name,
                        "lower_rate": rate,
                        "lower_rate_path": build_offer_path_less_than_rate(
                            row["zip_code"],
                            distributor.id,
                            row["rate_schedule"],
                            row["selected_offer_rate"],
                        ),
                    }
                )

        # Create the mailing_list DataFrame``
        mailing_df = pd.DataFrame(data)

        # Concatenate Subscriber DF if lower rates found
        if not mailing_df.empty:
            # If Rate Search returns a rate of 0 remove row
            mailing_df = self.remove_rows_with_zero(mailing_df, "lower_rate")
            # Remove any duplicates
            mailing_df = mailing_df.drop_duplicates()
            # Repeat subscriber DataFrame to match the number of lower offers/rates
            repeated_subscriber_row_df = self.row_series_to_multiple_row_df(
                row, len(mailing_df)
            )
            # Concatenating repeated_subscriber_row_df and mailing_df by row
            mailing_df = pd.concat([repeated_subscriber_row_df, mailing_df], axis=1)
        # No lower rates found, return empty DF
        else:
            column_names = [
                "email",
                "zip_code",
                "rate_schedule",
                "distributor_id",
                "selected_offer_rate",
                "lower_distributor_id",
                "lower_distributor_name",
                "lower_offer_name",
                "lower_rate",
                "lower_rate_path",
            ]
            mailing_df = pd.DataFrame(columns=column_names)

        return mailing_df

    def update_lower_rate_mailing_list_df(self):
        subscribers_df = self.get_all_subscribers()
        # Update PriceWatch subscribers_df attribute
        self.subscribers_df = subscribers_df

        mailing_df = pd.DataFrame()  # Create an empty DataFrame

        # For each subscriber, append lower rates/offers
        for index, row in subscribers_df.iterrows():
            lower_rates_df = self.build_lower_rate_mailing_list_df(row)
            mailing_df = pd.concat([mailing_df, lower_rates_df], ignore_index=True)

        mailing_df = mailing_df.dropna()
        # Update PriceWatch mailing_list_df attribute
        self.mailing_list_df = mailing_df
        return mailing_df
