from django.shortcuts import render, redirect
from django.urls import reverse
from web_parser.papowerswitch_api import papowerswitch_api
from web_parser.responses.ratesearch import price_structure
from django.http.request import HttpRequest
from django.http.response import HttpResponseForbidden, HttpResponse, JsonResponse
from web_parser.responses.ratesearch import offer
from GreenEnergySearch.models import User_Preferences
import json

def build_zip_search_path(zipcode):
     return reverse("green_energy_search:zip_search") + f"/?zipcode={zipcode}"

def build_rate_type_path(zipcode, distributor_id):
     return reverse("green_energy_search:rate_type") + f"/?zipcode={zipcode}&distributor_id={distributor_id}"

def build_offer_path(zipcode, distributor_id, rate_type):
    rate_type_query = rate_type.replace(" ", "+") # Replace any spaces with a + character to use as a query parameter.
    rate_type_query = rate_type_query.replace("%20", "+") # Replace any spaces with a + character to use as a query parameter.
    return reverse("green_energy_search:offer_search", kwargs={"zipcode":zipcode, "distributor_id":distributor_id, "rate_type":rate_type_query})

# Create your views here.
def zip_search(request):
    zipcode = request.GET.get('zipcode')
    # Get distributors from api using zipcode
    distributors = papowerswitch_api().get_distributors(zipcode)
    if len(distributors)==1: # Only one option, redirect to offersearch endpoint
        if len(distributors[0].rates)>1:
            # There are more than 1 rate to select from, redirect to let the user choose
            return redirect(build_rate_type_path(zipcode,distributors[0].id))
        return _handle_selected_distributor(zipcode, distributors[0])
    elif len(distributors)==0:
        return redirect(reverse('notfound'))
    else:
        return render(request, "GreenEnergySearch/home_zipsearch.html", {"distributors":distributors, "zipcode":zipcode, "show_modal":True})

def zip_search_distributor_selected(request):
    zipcode = request.GET.get('zipcode')
    distributor_id = request.GET.get('distributor_id')
    # Get distributors from api using zipcode
    distributors = papowerswitch_api().get_distributors(zipcode)
    # Get matching distributor
    for distributor in distributors:
        if str(distributor.id) == distributor_id:
            if len(distributor.rates)>1:
                return render(request, "GreenEnergySearch/home_zipsearch.html", {"distributors":[distributor], "zipcode":zipcode, "show_modal":True})
            else:
                return _handle_selected_distributor(zipcode, distributor)
    # No matching distributor
    return redirect(reverse('notfound'))
    
def _handle_selected_distributor(zipcode, distributor):
    if distributor!=None:
        num_rates = len(distributor.rates)
        if num_rates==0:
            # Rates shouldn't be 0, unexpected error
            return redirect(reverse('notfound'))
        elif num_rates==1:
            # There is only one rate option, there isn't anything the user can select.
            # Go straight to offer search
            return redirect(build_offer_path(zipcode,distributor.id,distributor.rates[0].rate_schedule))
    else:
        #If you've gotten here without a return something went wrong
        return redirect(reverse('notfound'))

def offer_search(request, zipcode, distributor_id, rate_type):
    api = papowerswitch_api()
    distributor = api.get_distributors(zipcode).find_distributor(distributor_id)
    if distributor is not None:
        offers = api.get_offers(distributor_id, rate_type)
        distributor_rate = distributor.get_rateschedule_rate(rate_type)
        def sorter(val):
            return val.rate
        filtered_offers = offers.filter(renewable_energy=True,
                                price_structure=price_structure.fixed,
                                upper_rate=distributor_rate.rate + 0.05)
        filtered_offers.sort(key=sorter)
        return render(request, "GreenEnergySearch/offers.html", {"offers": filtered_offers,
                                                                    "distributor":distributor,
                                                                    "distributor_rate":distributor_rate})
    else:
        return redirect(reverse('notfound'))

def possible_selections(request:HttpRequest):
    """Manage the possible selections endpoint"""
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Not authenticated")
    user_pref = User_Preferences.objects.get(user_id=request.user)
    if request.method == "DELETE":
        user_pref.clear_possible_selections()
        return HttpResponse("Possible Selections Cleared")
    if request.method == "GET":
        return JsonResponse(user_pref.possible_selections)
    elif request.method == "POST":
        # Add offer as a possible selection
        user_pref.add_possible_selection(offer(json.loads(request.body)))
        user_pref.save()
        return HttpResponse("Offer added!")
    
def current_selection(request:HttpRequest):
    """Manage the current selections endpoint"""
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Not authenticated")
    user_pref = User_Preferences.objects.get(user_id=request.user)
    if request.method == "DELETE":
        user_pref.selected_offer = dict
        user_pref.save()
    if request.method == "GET":
        return JsonResponse(user_pref.selected_offer)
    elif request.method == "PUT":
        user_pref.selected_offer = json.loads(request.body)
        user_pref.save()
        return HttpResponse("Offer selected!")
