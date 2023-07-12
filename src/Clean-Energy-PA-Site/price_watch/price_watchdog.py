from django.contrib.auth.models import User
from GreenEnergySearch.models import User_Preferences
from web_parser.papowerswitch_api import papowerswitch_api
from web_parser.responses.ratesearch import price_structure

api = papowerswitch_api()


class Price_Watch_Dog:
    def form_user_group(self):
        users = User.objects.all()
        zip_codes = []
        for user in users:
            try:
                user_preferences = User_Preferences.objects.get(
                    user_id=user, email_notifications=True
                )
                zip_codes.append(user_preferences.zip_code)
            except User_Preferences.DoesNotExist:
                pass
        return zip_codes

    def check_user_rates(self):
        zip_codes = self.form_user_group()
        for zip_code in zip_codes:
            distributors = api.get_distributors(zip_code)
            for distributor in distributors:
                print(f"zip_code: {zip_code}")
                distributor_id = distributor.id
                print(f"ID: {distributor_id}")
                distributor_rates = distributor.rates
                print(f"Rates: {distributor_rates}")
