from django.shortcuts import render, redirect
from django.urls import reverse
from web_parser import papowerswitch_api, price_structure


# Create your views here.
def build_offer_path_less_than_rate(zipcode, distributor_id, rate_type, less_than_rate):
    rate_type_query = rate_type.replace(
        " ", "+"
    )  # Replace any spaces with a + character to use as a query parameter.
    rate_type_query = rate_type_query.replace(
        "%20", "+"
    )  # Replace any spaces with a + character to use as a query parameter.
    return reverse(
        "email_scheduler:offer_search_less_than_rate",
        kwargs={
            "zipcode": zipcode,
            "distributor_id": distributor_id,
            "rate_type": rate_type_query,
            "less_than_rate": less_than_rate,
        },
    )


def offer_search_less_than_rate(
    request, zipcode, distributor_id, rate_type, less_than_rate
):
    api = papowerswitch_api()
    distributor = api.get_distributors(zipcode).find_distributor(distributor_id)
    if distributor is not None:
        offers = api.get_offers(distributor_id, rate_type)
        distributor_rate = distributor.get_rateschedule_rate(rate_type)

        # Filter resultsto only show rates lower than users rate
        def sorter(val):
            return val.rate

        filtered_offers = offers.filter(
            renewable_energy=True,
            price_structure=price_structure.fixed,
            upper_rate=float(less_than_rate),
        )
        filtered_offers.sort(key=sorter)

        return render(
            request,
            "EmailScheduler/offers.html",
            {
                "offers": filtered_offers,
                "distributor": distributor,
                "distributor_rate": distributor_rate,
                "less_than_rate": less_than_rate,
            },
        )
    else:
        return redirect(reverse("notfound"))
