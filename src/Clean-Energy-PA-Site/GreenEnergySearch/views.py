from django.shortcuts import render, redirect
from django.urls import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponseForbidden, HttpResponse, JsonResponse
from GreenEnergySearch.models import User_Preferences
from web_parser.responses import offer
from web_parser import price_structure, papowerswitch_api
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def build_zip_search_path(zipcode, save=False, redirect=None):
     save_query="&save=True" if save else ""
     redirect_query = f"&redirect={redirect}" if redirect != None else ""
     return reverse("green_energy_search:zip_search") + f"/?zipcode={zipcode}{save_query}{redirect_query}"

def build_rate_type_path(zipcode, distributor_id, save=False, redirect=None):
     save_query="&save=True" if save else ""
     redirect_query = f"&redirect={redirect}" if redirect != None else ""
     return reverse("green_energy_search:rate_type") + f"/?zipcode={zipcode}&distributor_id={distributor_id}{save_query}{redirect_query}"

def build_offer_path(zipcode, distributor_id, rate_type):
    rate_type_query = rate_type.replace(" ", "+") # Replace any spaces with a + character to use as a query parameter.
    rate_type_query = rate_type_query.replace("%20", "+") # Replace any spaces with a + character to use as a query parameter.
    return reverse("green_energy_search:offer_search", kwargs={"zipcode":zipcode, "distributor_id":distributor_id, "rate_type":rate_type_query})

# Create your views here.
def zip_search(request):
    zipcode = request.GET.get('zipcode')
    save = request.GET.get('save')
    redirect_url = request.GET.get('redirect')
    # Get distributors from api using zipcode
    distributors = papowerswitch_api().get_distributors(zipcode)
    if len(distributors)==1: # Only one option, redirect to offersearch endpoint
        if len(distributors[0].rates)>1:
            # There are more than 1 rate to select from, redirect to let the user choose
            return redirect(build_rate_type_path(zipcode,distributors[0].id, save, redirect_url))
        return _handle_selected_distributor(request, zipcode, distributors[0], bool(save), redirect_url)
    elif len(distributors)==0:
        return redirect(reverse('notfound'))
    else:
        return render(request, "GreenEnergySearch/home_zipsearch.html", {"distributors":distributors, "zipcode":zipcode, "show_modal":True, "save":save, "redirect":redirect_url})

def zip_search_distributor_selected(request):
    zipcode = request.GET.get('zipcode')
    distributor_id = request.GET.get('distributor_id')
    save = request.GET.get('save')
    redirect_url = request.GET.get('redirect')
    # Get distributors from api using zipcode
    distributors = papowerswitch_api().get_distributors(zipcode)
    # Get matching distributor
    for distributor in distributors:
        if str(distributor.id) == distributor_id:
            if len(distributor.rates)>1:
                return render(request, "GreenEnergySearch/home_zipsearch.html", {"distributors":[distributor], "zipcode":zipcode, "show_modal":True, "save":save, "redirect":redirect_url})
            else:
                return _handle_selected_distributor(request, zipcode, distributor, bool(save), redirect_url)
    # No matching distributor
    return redirect(reverse('notfound'))
    
def _handle_selected_distributor(request:HttpRequest, zipcode, distributor, save=False, redirect_url = None):
    if distributor!=None:
        num_rates = len(distributor.rates)
        if num_rates==0:
            # Rates shouldn't be 0, unexpected error
            return redirect(reverse('notfound'))
        elif num_rates==1:
            # There is only one rate option, there isn't anything the user can select.
            if request.user.is_authenticated and save:
                user_pref = User_Preferences.objects.get(user_id=request.user)
                user_pref.set_search_options(zipcode, distributor.id, distributor.name, distributor.rates[0].rate_schedule)
            if not redirect_url:
                # Go straight to offer search
                return redirect(build_offer_path(zipcode,distributor.id,distributor.rates[0].rate_schedule))
            else:
                return redirect(redirect_url)
    else:
        #If you've gotten here without a return something went wrong
        return redirect(reverse('notfound'))

def offer_search(request:HttpRequest, zipcode, distributor_id, rate_type):
    api = papowerswitch_api()
    distributor = api.get_distributors(zipcode).find_distributor(distributor_id)
    if distributor is not None:
        offers = api.get_offers(distributor_id, rate_type)
        distributor_rate = distributor.get_rateschedule_rate(rate_type)
        def sorter(val):
            return val.rate
        filtered_offers = offers.filter(renewable_energy=True,
                                price_structure= price_structure.fixed,
                                upper_rate=distributor_rate.rate + 0.05)
        filtered_offers.sort(key=sorter)
        current_contract=None
        if request.user.is_authenticated:
            user_pref = User_Preferences.objects.get(user_id=request.user)
            if user_pref.has_selected_offer():
                current_contract = user_pref.get_selected_offer() 
        return render(request, "GreenEnergySearch/offers.html", {"offers": filtered_offers,
                                                                    "distributor":distributor,
                                                                    "distributor_rate":distributor_rate,
                                                                    "current_contract":current_contract})
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
        if user_pref.add_possible_selection(offer(json.loads(request.body))):
            return HttpResponse("Offer added!")
        else:
            return HttpResponse("Offer already stored.")
    
def current_selection(request:HttpRequest):
    """Manage the current selections endpoint"""
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Not authenticated")
    user_pref = User_Preferences.objects.get(user_id=request.user)
    if request.method == "DELETE":
        user_pref.selected_offer = {}
        user_pref.save()
        return HttpResponse("Current selection successfully deleted.")
    if request.method == "GET":
        return JsonResponse(user_pref.selected_offer)
    elif request.method == "PUT":
        data = json.loads(request.body)
        _offer = offer(data)
        user_pref.selected_offer = data
        today = datetime.today()
        user_pref.selected_offer_selected_date = today
        end = today + relativedelta(months=int(_offer.term_length))
        user_pref.selected_offer_expected_end = end
        user_pref.save()
        return HttpResponse("Offer selected!")
    
def search_options(request:HttpRequest):
    """Manage the search options for a user"""
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Not authenticated")
    user_pref = User_Preferences.objects.get(user_id=request.user)
    if request.method == "DELETE":
        user_pref.distributor_id = -1
        user_pref.distributor_name = ""
        user_pref.rate_schedule = ""
        user_pref.save()
        return HttpResponse("Search Options successfully cleared.")
    if request.method == "GET":
        return JsonResponse({"zipcode":user_pref.zip_code,
                                "distributor":{
                                    "id":user_pref.distributor_id,
                                    "name":user_pref.distributor_name
                                },
                                "rate_schedule":user_pref.rate_schedule})
    elif request.method == "PUT":
        data = json.loads(request.body)
        zip_code = str(data["zip_code"])
        distributor_id = int(data["distributor_id"])
        distributor_name = papowerswitch_api().get_distributors(zip_code=zip_code).find_distributor(distributor_id).name
        rate_schedule = str(data["rate_schedule"])
        user_pref.set_search_options(zip_code, distributor_id, distributor_name, rate_schedule)
        return HttpResponse("Search Options saved!")
    
class PossibleSelectionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request:HttpRequest):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        if request.user.is_authenticated and "user/preferences/" not in request.path:
            user_pref = User_Preferences.objects.get(user_id=request.user)
            poss_sel = user_pref.get_possible_selections()
            if len(poss_sel)>0:
                time_del = datetime.now() - poss_sel.last_updated
                if time_del.days<180: # less than 6 months
                    return render(request, "GreenEnergySearch/possible_selections.html", {"possible_selections": poss_sel.offers,
                                                                                            "redirect": request.path,
                                                                                            "show_modal":True})
                else:
                    user_pref.clear_possible_selections()
        # Code to be executed for each request/response after
        # the view is called.

        return response