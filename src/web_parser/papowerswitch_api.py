import requests
import json
import api_settings

class papowerswitch_api:
    failed_preface = "Request failed with status code:"
    request_log_preface = "Retrieving from the following endpoint:"
    base_url = api_settings.base_url
    zip_seach_endpoint = "ZipSearch"
    rates_endpoint = "Rates"

    def get(self, endpoint):
        return requests.get(self.base_url + endpoint)
    
    def get_residential_from_zipcode(self, zip_code:str|int):
        service_type = "residential" #TODO: may want to pull this out as a parameter
        endpoint = self.zip_seach_endpoint + "?zipcode=" + str(zip_code)  + "&servicetype=" +service_type
        return self.get(endpoint)
    
    def get_rates_from_id(self, id:str|int):
        service_type = "residential"
        rate_type = "R+-+Regular+Residential+Service"
        endpoint = self.zip_seach_endpoint + "?id=" + str(id)  + "&servicetype=" +service_type + "&ratetype=" + rate_type
        return self.get(endpoint)
    
    def get_search_id(self, zip_code:str|int):
        response = self.get_residential_from_zipcode(zip_code)
        if response.status_code == 200:
            data = response.json()
            return data[0]['id']
        # Process the data
        else:
            print(self.failed_preface, response.status_code)
    
    def get_peco_rate(self, zip_code:str|int):
        response = self.get_residential_from_zipcode(zip_code)
        if response.status_code == 200:
            data = response.json()
            return data[0]['Rates'][0]['Rate']
            # Process the data
        else:
            print(self.failed_preface, response.status_code)

    def get_options(self, id:str|int, peco_rate:float):
        response = self.get_rates_from_id(id)
        if response.status_code == 200:
            data = response.json()
            # Filter the JSON body by multiple attributes
            filtered_data = [obj for obj in data 
            if obj["RenewableEnergy"] == True and 
            obj["RenewablePercentage"] == 100 and
            obj["PriceStructure"] == "fixed" and
            obj["MonthlyFee"] == False and
            obj["MonthlyFeeAmount"] == "" and
            obj["CancellationFee"] == "" and 
            obj["EnrollmentFee"] == False and
            obj["Rate"] < peco_rate # need to dynamically get that PECO rate still
            ]

            # Sort by lowest 

            # Sort the JSON array based on the "id" attribute
            sorted_data = sorted(filtered_data, key=lambda x: x["Rate"])

            # Convert the sorted data back to JSON
            sorted_json_array = json.dumps(sorted_data)

            return sorted_json_array

        else:
            print("Request failed with status code:", response.status_code)