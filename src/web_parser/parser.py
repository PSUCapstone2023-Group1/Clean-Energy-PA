from papowerswitch_api import papowerswitch_api

zip_code = 19473

api = papowerswitch_api()
print(api.get_peco_rate(zip_code))

search_id = api.get_search_id(zip_code)
peco_rate = api.get_peco_rate(zip_code)

options = api.getOptions(search_id, peco_rate)
print(options)