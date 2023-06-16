#Need to append root to sys path
from papowerswitch_api import papowerswitch_api
import zipsearch_test_data
import ratesearch_test_data
import api_settings
import requests_mock
import requests
import pytest


class TestBaseRequests:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.api = papowerswitch_api()

    def test_get_noendpoint(self, requests_mock:requests_mock.Mocker):
        requests_mock.get(api_settings.base_url, status_code=404)
        response:requests.Response = self.api.get("")
        assert response.status_code == 404

    def test_get_zipsearch(self, requests_mock:requests_mock.Mocker):
        requests_mock.get(api_settings.base_url + api_settings.zip_seach_endpoint, status_code=404)
        response:requests.Response = self.api.get(api_settings.zip_seach_endpoint)
        assert response.status_code == 404
    
    def test_get_rates(self, requests_mock:requests_mock.Mocker):
        requests_mock.get(api_settings.base_url+ api_settings.rates_endpoint, status_code=404)
        response:requests.Response = self.api.get(api_settings.rates_endpoint)
        assert response.status_code == 404

class TestZipSearch:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.api = papowerswitch_api()
        self.endpoint = api_settings.base_url+ api_settings.zip_seach_endpoint
        self.test_zipcode = 19473

    def test_get_residential_from_zipcode_expected(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.expected_example)
        response:requests.Response = self.api.get_distributors_from_zipcode(self.test_zipcode)
        assert response.status_code == 200
        assert response.json != None
    
    def test_get_residential_from_zipcode_unexpected(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.unexpected_example)
        response:requests.Response = self.api.get_distributors_from_zipcode(self.test_zipcode)
        assert response.status_code == 200
        assert response.json != None

    def test_get_search_id_success(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.expected_example)
        searchid = self.api.get_search_id(self.test_zipcode)
        assert searchid == str(zipsearch_test_data.expected_example[0]["id"])
    
    def test_get_search_id_fail(self, requests_mock:requests_mock.Mocker): 
        with pytest.raises(ValueError):
            requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.unexpected_example)
            self.api.get_search_id(self.test_zipcode)

    def test_get_peco_rate_success(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.expected_example)
        rate = self.api.get_peco_rate(self.test_zipcode)
        assert rate == zipsearch_test_data.expected_example[0]["Rates"][0]["Rate"]
    
    def test_get_peco_rate_fail(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=zipsearch_test_data.unexpected_example)
        with pytest.raises(ValueError):
            self.api.get_peco_rate(self.test_zipcode)

class TestRatesearch:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.api = papowerswitch_api()
        self.endpoint = api_settings.base_url+ api_settings.rates_endpoint
        self.test_searchid = 1
    
    def test_get_rates_from_id_expected(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=ratesearch_test_data.expected_example)
        response:requests.Response = self.api.get_rates_from_id(self.test_searchid)
        assert response.status_code == 200
        assert response.json != None
    
    def test_get_get_rates_from_id_unexpected(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=ratesearch_test_data.unexpected_example)
        response:requests.Response = self.api.get_rates_from_id(self.test_searchid)
        assert response.status_code == 200
        assert response.json != None

    def test_get_options_expected(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=ratesearch_test_data.expected_example)
        options = self.api.get_options(self.test_searchid, 1)
        # Filter worked for one of the options
        assert len(options)>0
        # Shows filter worked for second option
        assert options[0].id == str(ratesearch_test_data.expected_example[1]["id"])
        
    
    def test_get_get_options_unexpected(self, requests_mock:requests_mock.Mocker): 
        requests_mock.get(self.endpoint, status_code=200, json=ratesearch_test_data.unexpected_example)
        with pytest.raises(ValueError):
            self.api.get_options(self.test_searchid, 0.1)
        