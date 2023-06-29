from django.shortcuts import render, redirect
from django.urls import reverse
from web_parser.papowerswitch_api import papowerswitch_api
from web_parser.responses.ratesearch import price_structure

# Create your views here.
def home(request):
    return render(request, "GreenEnergySearch/home.html", {})

def zip_search(request):
    zipcode = request.GET.get('zipcode')
    # Get distributors from api using zipcode
    distributors = papowerswitch_api().get_distributors(zipcode)
    if len(distributors)==1: # Only one option, redirect to offersearch endpoint
        if len(distributors[0].rates)>1:
            # There are more than 1 rate to select from, redirect to let the user choose
            return redirect(reverse('green_energy_search:rate_type'), zipcode=zipcode, distributor_id=distributors[0].id)
        return _handle_selected_distributor(distributors[0])
    elif len(distributors)==0:
        return redirect(reverse('404'))
    else:
        return render(request, "GreenEnergySearch/home_zipsearch.html", {"distributors":distributors, "zipcode":zipcode})

def zip_search_distributor_selected(request):
    zipcode = request.GET.get('zipcode')
    distributor_id = request.GET.get('distributor_id')
    # Get distributors from api using zipcode
    distributors = papowerswitch_api().get_distributors(zipcode)
    # Get matching distributor
    for distributor in distributors:
        if str(distributor.id) == distributor_id:
            if len(distributor.rates)>1:
                return render(request, "GreenEnergySearch/home_zipsearch.html", {"distributors":[distributor], "zipcode":zipcode})
            else:
                return _handle_selected_distributor(distributor)
    # No matching distributor
    return redirect(reverse('404'))
    
def _handle_selected_distributor(distributor):
    if distributor!=None:
        num_rates = len(distributor.rates)
        if num_rates==0:
            # Rates shouldn't be 0, unexpected error
            return redirect(reverse('404'))
        elif num_rates==1:
            # There is only one rate option, there isn't anything the user can select.
            # Go straight to offer search
            return redirect(reverse('green_energy_search:offer_search',
                            kwargs={
                                "distributor_id":distributor.id,
                                "rate_type":distributor.rates[0].rate_schedule
                                }))
    else:
        #If you've gotten here without a return something went wrong
        return redirect(reverse('404'))

def offer_search(request, zipcode, distributor_id, rate_type):
    api = papowerswitch_api()
    distributor = api.get_distributors(zipcode).find_distributor(distributor_id)
    if distributor is not None:
        offers = api.get_offers(distributor_id, rate_type)
        filtered_offers = offers.filter(renewable_energy=True,
                                price_structure=price_structure.variable,
                                upper_rate=distributor.get_rateschedule_rate(rate_type).rate + 0.05)
        return render(request, "GreenEnergySearch/offers.html", {"offers": filtered_offers})
    else:
        return redirect('404')