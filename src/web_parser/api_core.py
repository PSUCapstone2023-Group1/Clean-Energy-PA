import requests
import api_settings

service_type = "residential" # Will always be residential for us, can be hardcoded

class api_core:
    def get(self, endpoint):
        return requests.get(api_settings.base_url + endpoint)
    
    def get_zipsearch_endpoint(self, zip_code:str|int):
        """
        Make a get request to the zipsearch endpoint
        
        This endpoint is used to find the distributors for a given zip code and service type (always residential for us)

        Parameters:
            zip_code (str|int): The zip code to search against

        Returns:
            Response: The response object of the get request
        """
        endpoint = api_settings.zip_seach_endpoint + "?zipcode=" + str(zip_code)  + "&servicetype=" + service_type
        return self.get(endpoint)
    
    def get_rates_endpoint(self, distributor_id:str|int, rate_type:str):
        """
        Make a get request to the rates endpoint.
        
        This endpoint is used to get the current rate options for a given distributor, service type (always residential for us), and rate type

        Parameters:
            distributor_id (str|int): The api id of the selected distributor

            rate_type (str): The rate schedule selected

        Returns:
            Response: The response object of the get request
        """
        rate_type_query = rate_type.replace(" ", "+") # Replace any spaces with a + character to use as a query parameter.
        rate_type_query = rate_type_query.replace("%20", "+") # Replace any spaces with a + character to use as a query parameter.
        endpoint = api_settings.rates_endpoint + "?id=" + str(distributor_id)  + "&servicetype=" + service_type + "&ratetype=" + rate_type_query
        return self.get(endpoint)