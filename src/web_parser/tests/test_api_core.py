#Need to append root to sys path
from api_core import api_core
import api_settings
import requests_mock
import requests
import pytest


class TestBaseRequests:

    @pytest.fixture(autouse=True)
    def before_each(self):
        self.api = api_core()

    def test_get_noendpoint(self, requests_mock:requests_mock.Mocker):
        "Verify that the base get request doesn't throw an exception and gives the expected status code"
        requests_mock.get(api_settings.base_url, status_code=404)
        response:requests.Response = self.api.get("")
        assert response.status_code == 404

    def test_get_zipsearch(self, requests_mock:requests_mock.Mocker):
        "Verify that the zipsearch endpoint get request doesn't throw an exception and gives the expected status code"
        requests_mock.get(api_settings.base_url + api_settings.zip_seach_endpoint, status_code=404)
        response:requests.Response = self.api.get(api_settings.zip_seach_endpoint)
        assert response.status_code == 404
    
    def test_get_rates(self, requests_mock:requests_mock.Mocker):
        "Verify that the ratesearch endpoint get request doesn't throw an exception and gives the expected status code"
        requests_mock.get(api_settings.base_url+ api_settings.rates_endpoint, status_code=404)
        response:requests.Response = self.api.get(api_settings.rates_endpoint)
        assert response.status_code == 404        