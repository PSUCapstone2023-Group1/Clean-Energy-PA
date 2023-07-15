from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from web_parser.papowerswitch_api import papowerswitch_api
from web_parser.responses.ratesearch import price_structure
import pandas as pd

api = papowerswitch_api()


class Price_Watch_Dog:
    # build group {email_notifications, zip_code, rate_type}
    # 2 tables key pair (distributor_id, rate_type)
    # thread that compares based on groups found
    # passing the model data from django to pricewatch

    def get_all_subscribers(self):
        """Returns a dataframe of subscribers
        (folks who selected True for email notifications)"""
        users = User.objects.all()
        subscribed_users = []
        for user in users:
            try:
                user_preferences = User_Preferences.objects.get(
                    user_id=user, email_notifications=True
                )
                subscribed_users.append(
                    {
                        "user_id": user_preferences.user_id,
                        "zip_code": user_preferences.zip_code,
                        "rate_schedule": user_preferences.rate_schedule,
                        "distributor_id": user_preferences.distributor_id,
                        "selected_offer_id": user_preferences.selected_offer_id,
                        "selected_offer_rate": user_preferences.selected_offer_rate,
                    }
                )
            except User_Preferences.DoesNotExist:
                pass
        subscribers_df = pd.DataFrame(subscribed_users)
        return subscribers_df

    def get_unique_rate_search_params(self, df):
        """returns a dataframe that represents all unique combinations"""
        df = df.drop(columns=["user_id", "selected_offer_id"], axis=1)
        df = df.reset_index(drop=True)
        # Specify the columns you want to consider for uniqueness
        columns_to_check = [
            "zip_code",
            "rate_schedule",
            "distributor_id",
            "selected_offer_rate",
        ]
        # Drop duplicates based on the specified columns
        df = df.drop_duplicates(subset=columns_to_check)
        print(df)
        return df

    def check_user_rates(self):
        subscribers_df = self.get_all_subscribers()
        unique_rate_search_df = self.get_unique_rate_search_params(subscribers_df)

        # for zip_code in zip_codes:
        #     distributors = api.get_distributors(zip_code)
        #     print(f"There are {len(distributors)} distributors")
        #     for distributor in distributors:
        #         print(f"zip_code: {zip_code}")
        #         rates = distributor.rates
        #         print(f"There are {len(rates)} rates")
        #         for rate in rates:
        #             print(f"Rate: {rate.id}")
        #             offers = api.get_offers(rate.id, "R - Regular Residential Service")
        #             print(f"There are {len(offers)} offers")
        #             for offer in offers:
        #                 print(f"Offer: {offer}")
