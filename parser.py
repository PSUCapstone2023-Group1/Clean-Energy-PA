import requests
import json



zip = 19473

def getSearchID(zip):
    url = "https://www.papowerswitch.com/umbraco/Api/ShopApi/ZipSearch?zipcode=" + str(zip)  + "&servicetype=residential"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data[0]['id']
        # Process the data
    else:
        print("Request failed with status code:", response.status_code)


def getOptions(searchID):

    url = "https://www.papowerswitch.com/umbraco/Api/ShopApi/Rates?id=" + str(searchID) + "&servicetype=residential&ratetype=R+-+Regular+Residential+Service"

    response = requests.get(url)

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
        obj["Rate"] < 0.9726 # need to dynamically get that PECO rate still

        ]

        # Sort by lowest 

        # Sort the JSON array based on the "id" attribute
        sorted_data = sorted(filtered_data, key=lambda x: x["Rate"])

            # Convert the sorted data back to JSON
        sorted_json_array = json.dumps(sorted_data)


        return sorted_json_array

    else:
        print("Request failed with status code:", response.status_code)

options = getOptions(getSearchID(zip))
print(options)
