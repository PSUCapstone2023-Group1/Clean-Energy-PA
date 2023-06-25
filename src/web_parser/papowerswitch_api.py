import requests
from api_core import api_core
from responses.ratesearch import offer_collection
from responses.zipsearch import distributor_collection
from typing import Union

class papowerswitch_api:
    failed_preface = "Request failed with status code:"
    api: api_core

    def __init__(self):
        self.api = api_core()

    def get_distributors(self, zip_code:Union[str,int]):
        """
        Make a get request to the zipsearch endpoint and realize a (200) OK message into a list of zipsearch response objects

        Parameters:
            zip_code (str|int): The zip code to search against

        Returns:
            distributor_collection: A collection handler for the distributor object

        Exceptions:
            requests.exceptions.HTTPError: If not (200) OK response
            ValueError: If the response json is not parsable as expected
        """
        response:requests.Response = self.api.get_zipsearch_endpoint(zip_code)
        if response.status_code == 200:
            data = distributor_collection(response.json()) #convert json to a distributor collection
            return data
        else:
            print(self.failed_preface, response.status_code)
            response.raise_for_status()
            

    def get_offers(self, id:Union[str,int], rate_type:str):
        """
        Make a get request to the rates endpoint and realize a (200) OK message into a list of ratesearch response objects

        Parameters:
            distributor_id (str|int): The api id of the selected distributor

            rate_type (str): The rate schedule selected

        Returns:
            offer_collection: A collection handler for the offer object

        Exceptions:
            requests.exceptions.HTTPError: If not (200) OK response
            ValueError: If the response json is not parsable as expected
        """
        response:requests.Response = self.api.get_rates_endpoint(id, rate_type)
        if response.status_code == 200:
            data = offer_collection(response.json()) #convert json to an offer collection
            return data
        else:
            print(self.failed_preface, response.status_code)
            response.raise_for_status()