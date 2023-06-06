from api import api

zip_code = 19473

papowerswitch_api = api()
print(papowerswitch_api.get_peco_rate(zip_code))

search_id = papowerswitch_api.get_search_id(zip_code)
peco_rate = papowerswitch_api.get_peco_rate(zip_code)

options = papowerswitch_api.getOptions(search_id, peco_rate)
print(options)