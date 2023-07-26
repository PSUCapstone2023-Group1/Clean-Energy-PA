from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import pandas as pd
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance
from EmailScheduler.contract_watch.contract_watchdog_instance import (
    Contract_Watch_Dog_Instance,
)


class Email_Batch:
    def __init__(self):
        self.send_lower_rate_email_return = 0
        self.send_contract_end_email_return = 0

    def get_first_name(self, email):
        user = User.objects.get(email=email)
        return user.first_name, user

    def get_rate(self, user):
        # Get their preferences from db for email content
        user_preferences = User_Preferences.objects.get(user_id=user)
        selected_offer = user_preferences.get_selected_offer()
        return selected_offer.rate, user_preferences

    def limit_results_output(self, df, sort_col, group_col, head_num):
        # Sort dataframe
        df = df.sort_values(by=sort_col, ascending=True)
        # Group dataframe
        df = df.groupby(group_col).apply(
            lambda group: group.drop_duplicates().head(head_num)
        )
        # Reset the index
        df.reset_index(drop=True, inplace=True)
        return df

    def send_lower_rate_emails(self):
        # Get Subscribers and Mailing list
        subscribers_df = Price_Watch_Dog_Instance.subscribers_df
        mailing_list_df = Price_Watch_Dog_Instance.mailing_list_df

        # Iterate over each row in the Subscribers DataFrame
        for _, row in subscribers_df.iterrows():
            email = str(row["email"])
            lower_rate_offers_df = pd.DataFrame()

            # Slice the DataFrame based on the email column
            lower_rate_offers_df = mailing_list_df[mailing_list_df["email"] == email]

            # If the DataFrame is empty skip this email
            if len(lower_rate_offers_df) == 0:
                continue

            # Limit the output
            lower_rate_offers_df = self.limit_results_output(
                lower_rate_offers_df,  # Sort ascending on rate
                "lower_rate",  # Groupby distributor
                "lower_distributor_name",
                3,  # Top 3 from each distributor
            )

            # Get First Name and User
            first_name, user = self.get_first_name(email)
            # Get rate and User_Pref
            rate, user_preferences = self.get_rate(user)

            # Render the HTML template with the dynamic values
            html_content = render_to_string(
                "lower_rate_email.html",
                {
                    "first_name": first_name,
                    "rate": rate,
                    "lower_rate_offers": lower_rate_offers_df,
                    "domain": settings.CURRENT_DOMAIN,
                },
            )

            # Compose your email content and subject
            subject = "Lower Energy Rates Found!"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            # Send the email using Django's send_mail function
            self.send_lower_rate_email_return = send_mail(
                subject, "", from_email, recipient_list, html_message=html_content
            )

    def send_contract_expiration_emails(self):
        contract_expiration_df = Contract_Watch_Dog_Instance.contract_end_dates_df
        lower_contract_options_df = (
            Contract_Watch_Dog_Instance.lower_contract_options_df
        )
        for _, row in contract_expiration_df.iterrows():
            email = row["email"]

            lower_contract_offers_df = lower_contract_options_df[
                lower_contract_options_df["email"] == email
            ]

            # Limit the output,
            lower_contract_offers_df = self.limit_results_output(
                lower_contract_offers_df,
                "lower_rate",  # Sort ascending on rate
                "lower_distributor_name",  # Groupby distributor
                3,  # Top 3 from each distributor
            )

            contract_end_date = row["contract_end_date"]
            days_left = row["days_left"]

            # Get First Name and User
            first_name, user = self.get_first_name(email)
            # Get rate and User_Pref
            try:
                rate, user_preferences = self.get_rate(user)
            except:
                # offer doesnt exist for user
                pass
            last_updated = user_preferences.get_selected_offer().last_updated
            print("running")

            # Render the HTML template with the dynamic values
            html_content = render_to_string(
                "contract_expiration_email.html",
                {
                    "first_name": first_name,
                    "rate": rate,
                    "contract_end_date": last_updated,
                    "days_left": days_left,
                    "lower_contract_offers": lower_contract_offers_df,
                    "domain": settings.CURRENT_DOMAIN,
                },
            )

            # Compose your email content and subject
            subject = f"Contract Ending in {days_left} Days!"

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            if days_left == 30 or days_left == 14 or days_left == 2:
                self.send_contract_end_email_return = send_mail(
                    subject, "", from_email, recipient_list, html_message=html_content
                )
            else:
                continue
