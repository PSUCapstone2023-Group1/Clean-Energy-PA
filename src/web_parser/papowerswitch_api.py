import requests
from api_core import api_core
from responses.ratesearch import ratesearch_response
from responses.zipsearch import zipsearch_response

class papowerswitch_api:
    failed_preface = "Request failed with status code:"
    api_core = api_core()

    def get_distributors(self, zip_code:str|int):
        """
        Make a get request to the zipsearch endpoint and realize a (200) OK message into a list of zipsearch response objects

        Parameters:
            zip_code (str|int): The zip code to search against

        Returns:
            list[zipsearch_response]: A list of zipsearch_response objects

        Exceptions:
            requests.exceptions.HTTPError: If not (200) OK response
            ValueError: If the response json is not parsable into a list of zipsearch_responses
        """
        response:requests.Response = api_core.get_zipsearch_endpoint(zip_code)
        if response.status_code == 200:
            data = list(map(lambda x: zipsearch_response(x), response.json())) #convert json to zipsearch_response objects
            return data
        else:
            print(self.failed_preface, response.status_code)
            response.raise_for_status()
            

    def get_options(self, id:str|int, rate_type:str):
        """
        Make a get request to the rates endpoint and realize a (200) OK message into a list of ratesearch response objects

        Parameters:
            distributor_id (str|int): The api id of the selected distributor

            rate_type (str): The rate schedule selected

        Returns:
            list[ratesearch_response]: The response object 

        Exceptions:
            requests.exceptions.HTTPError: If not (200) OK response
            ValueError: If the response json is not parsable into a list of ratesearch_responses
        """
        response:requests.Response = api_core.get_rates_endpoint(id, rate_type)
        if response.status_code == 200:
            data = list(map(lambda x: ratesearch_response(x), response.json())) #convert json to ratesearch_response objects
            return data
        else:
            print(self.failed_preface, response.status_code)
            response.raise_for_status()