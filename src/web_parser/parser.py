from papowerswitch_api import papowerswitch_api
from responses.zipsearch import zipsearch_response
import tests.zipsearch_test_data
import api_settings

zip_code = 19473

api = papowerswitch_api()

print(api.get(api_settings.zip_seach_endpoint))

residential = api.get_distributors_from_zipcode(zip_code)
print('Residential Response:', residential.json())
search_id = api.get_search_id(zip_code)
peco_rate = api.get_peco_rate(zip_code)

print('Search_Id:', search_id)
print('Peco Rate:', peco_rate)

options = api.get_options(search_id, peco_rate)
for option in options:
    print(option.__str__())