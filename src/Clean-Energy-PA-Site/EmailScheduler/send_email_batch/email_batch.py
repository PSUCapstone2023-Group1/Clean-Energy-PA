from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import pandas as pd
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance


class Email_Batch:
    def __init__(self):
        self.send_email_return = 0
        pass

    def send_lower_rate_emails(self):
        # Get Subscribers and Mailing list
        subscribers_df = Price_Watch_Dog_Instance.subscribers_df
        mailing_list_df = Price_Watch_Dog_Instance.mailing_list_df

        # Iterate over each row in the Subscribers DataFrame
        for _, row in subscribers_df.iterrows():
            email = str(row["email"])
            lower_rate_offers_df = pd.DataFrame()
            try:
                # Slice the DataFrame based on the email column
                lower_rate_offers_df = mailing_list_df[
                    mailing_list_df["email"] == email
                ]

                # Drop distributors to not overwhelm the user
                # Only keep the first distributor even if there are more offers
                # The link redirects them to all offers
                lower_rate_offers_df = lower_rate_offers_df.drop_duplicates(
                    subset="lower_distributor_name", keep="first"
                )
            except:
                # TODO: Handle exception
                pass

            # Get the user by email
            user = User.objects.get(email=email)
            # Get their first name from db for email content
            first_name = user.first_name

            # Get their preferences from db for email content
            user_preferences = User_Preferences.objects.get(user_id=user)
            selected_offer = user_preferences.get_selected_offer()
            rate = selected_offer.rate

            # Render the HTML template with the dynamic values
            html_content = render_to_string(
                "lower_rate_email.html",
                {
                    "first_name": first_name,
                    "rate": rate,
                    "lower_rate_offers": lower_rate_offers_df,
                    "domain": "http://127.0.0.1:8000",  # TODO: Figure out how to make this agnostic
                },
            )

            # Compose your email content and subject
            subject = "Lower Energy Rates Found!"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            # Send the email using Django's send_mail function
            self.send_email_return = send_mail(
                subject, "", from_email, recipient_list, html_message=html_content
            )
