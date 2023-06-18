#Need to append root to sys path
from papowerswitch_api import papowerswitch_api
import zipsearch_test_data
import ratesearch_test_data
import api_settings
import requests_mock
import requests
import pytest
from responses.ratesearch import offer_collection
from responses.zipsearch import distributor_collection

class TestZipSearch:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.api = papowerswitch_api()
        self.endpoint = api_settings.base_url+ api_settings.zip_seach_endpoint
        self.test_zipcode = 19473

    def test_get_distributors_expected(self, requests_mock:requests_mock.Mocker): 
        "Verify a 200 response with an expected message builds the collection correctly"
        requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.expected_example)
        distributors = self.api.get_distributors(self.test_zipcode)
        assert len(distributors)>0
        assert distributors[0].id == str(zipsearch_test_data.expected_example[0]["id"])
    
    def test_get_distributors_unexpected(self, requests_mock:requests_mock.Mocker):
        "Verify a 200 response with an unexpected message raises a Value Error"
        with pytest.raises(ValueError):
            requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.unexpected_example)
            self.api.get_distributors(self.test_zipcode)

    def test_get_distributors_404(self, requests_mock:requests_mock.Mocker): 
        "Verify a 404 error raises an HTTP Error"
        with pytest.raises(requests.exceptions.HTTPError):
            requests_mock.get(self.endpoint, status_code=404)
            self.api.get_distributors(self.test_zipcode)

    def test_distributor_collection_iterable(self):
        "Verify that the distributor collection is iterable"
        distributors = distributor_collection(zipsearch_test_data.expected_example)
        for distributor in distributors:
            assert str(distributor) == str(zipsearch_test_data.expected_example[0]["id"]) + ": " + str(zipsearch_test_data.expected_example[0]["Name"])
            assert str(distributor.rates[0]) == str(zipsearch_test_data.expected_example[0]["Rates"][0]["id"])

class TestRatesearch:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.api = papowerswitch_api()
        self.endpoint = api_settings.base_url+ api_settings.rates_endpoint
        self.test_searchid = 1
        self.test_ratetype = "R - Regular Residential Service"

    def test_get_offers_expected(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=ratesearch_test_data.expected_example)
        offers = self.api.get_offers(self.test_searchid, self.test_ratetype)
        # Gets both offers
        assert len(offers)==2
        # Shows we get 
        assert offers[0].id == str(ratesearch_test_data.expected_example[0]["id"])
        
    
    def test_get_get_offers_unexpected(self, requests_mock:requests_mock.Mocker):
        requests_mock.get(self.endpoint, status_code=200, json=ratesearch_test_data.unexpected_example)
        with pytest.raises(ValueError):
            self.api.get_offers(self.test_searchid, self.test_ratetype)

    def test_get_offers_404(self, requests_mock:requests_mock.Mocker): 
        "Verify a 404 error raises an HTTP Error"
        with pytest.raises(requests.exceptions.HTTPError):
            requests_mock.get(self.endpoint, status_code=404)
            self.api.get_offers(self.test_searchid, self.test_ratetype)
    
    def test_filter_offers(self):
        "Verify that the filter works as expected"
        data = ratesearch_test_data.expected_example[1]
        offers = offer_collection(ratesearch_test_data.expected_example)
        filtered_offers = offers.filter(name=data["Name"],
                    renewable_pa= data["RenewablePA"],
                    solar=data["Solar"],
                    introductory_price=data["IntroductoryPrice"],
                    discount_available=data["DiscountAvailable"],
                    net_metering=data["NetMetering"],
                    pa_wind=data["PAWind"],
                    renewable_energy=data["RenewableEnergy"],
                    lower_renewable_percentage=0, # Set to the minimum
                    price_structure=data["PriceStructure"],
                    monthly_fee=data["MonthlyFee"],
                    monthly_fee_amount=data["MonthlyFeeAmount"],
                    cancellation_fee=data["CancellationFee"],
                    enrollment_fee=data["EnrollmentFee"],
                    upper_rate=1 # Use a large rate
                    )
        assert len(filtered_offers)==1
        assert str(filtered_offers[0].id) == str(data["id"])
        assert str(filtered_offers[0]) == str(data["id"]) + ": " + str(data["Name"])