from papowerswitch_api import papowerswitch_api
from responses.ratesearch import price_structure

zip_code = 19473

api = papowerswitch_api()

distributors = api.get_distributors(zip_code)

selected_distributor = distributors[0]
selected_rate = selected_distributor.rates[0]

print('Search_Id:', selected_distributor.id)
print('Selected Distributor Rate:', selected_distributor.rates[0].rate)

offers = api.get_offers(selected_distributor.id, selected_rate.rate_schedule)

filtered_offers = offers.filter(price_structure=price_structure.fixed, upper_rate=1)

print("Total Offers Count:", len(offers))
print("Filtered Offers Count:", len(filtered_offers))
for filtered_offers in filtered_offers:
    print(filtered_offers.__str__())