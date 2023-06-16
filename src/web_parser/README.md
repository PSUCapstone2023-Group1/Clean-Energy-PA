# Summary

This intent of the web_parser package is to provide a simple programming api to make requests to the `www.papowerswitch.com/umbraco/API/ShopAPI` REST api.

> **Note:** We were unable to find documentation for this API and therefore, the endpoints that we needed were determined by watching the network traffic as we navigated [www.papowerswitch.com](www.papowerswitch.com) for options.

## Table of Contents

- [Summary](#summary)
  - [Table of Contents](#table-of-contents)
  - [Endpoints](#endpoints)
    - [ZipSearch](#zipsearch)
      - [ZipSearch Query](#zipsearch-query)
      - [ZipSearch Response Example](#zipsearch-response-example)
    - [Rates](#rates)
      - [Rates Query](#rates-query)
      - [Rates Response Example](#rates-response-example)

## Endpoints

---

As mentioned above the base url for the REST API is `www.papowerswitch.com/umbraco/API/ShopAPI`.

The endpoints we will be accessing are:

- ZipSearch
  - Gets a list of distributor objects available for a zipcode and service type provided.
- Rates
  - Gets a list of rate options for a distributor id and rate schedule provided.

These endpoints are discussed in more detail below.

### ZipSearch

---

#### ZipSearch Query

This endpoint can be accessed by the base URL (described above) plus `/ZipSearch`

This endpoint requires a query be provided and the query string has two inputs

1. `zipcode` - A valid PA zipcode, if the zipcode is invalid it will return a (200) success message with an empty array in the body.
2. `servicetype` - The type of service that you are searching for, for our purposes we will hardcode "residential".

Valid request example:

```http
www.papowerswitch.com/umbraco/Api/ShopApi/ZipSearch?zipcode=15025&servicetype=residential
```

#### ZipSearch Response Example

200 - OK

```json
[
  {
    "id": 27487,
    "Name": "Duquesne Light",
    "Phone": "412-393-7100",
    "Website": "https://www.duquesnelight.com",
    "Rates": [
      {
        "id": 27489,
        "RateSchedule": "RA - Residential Add - on Heat Pump Service",
        "Rate": 0.1099,
        "PastRates": [
          {
            "Key": "2015-12-01",
            "Value": 0.0754
          }
        ],
        "FutureRate": 0.0,
        "FutureRateTimeframe": "This will be the actual price beginning December 01, 2023",
        "LastUpdatedDate": "May 25, 2023"
      },
      {
        "id": 27490,
        "RateSchedule": "RH - Residential Heating Service",
        "Rate": 0.104,
        "PastRates": [
          {
            "Key": "2015-12-01",
            "Value": 0.0712
          }
        ],
        "FutureRate": 0.0,
        "FutureRateTimeframe": "This will be the actual price beginning December 01, 2023",
        "LastUpdatedDate": "May 25, 2023"
      },
      {
        "id": 27488,
        "RateSchedule": "RS - Regular Residential Service",
        "Rate": 0.1145,
        "PastRates": [
          {
            "Key": "2015-06-01",
            "Value": 0.0798
          }
        ],
        "FutureRate": 0.0,
        "FutureRateTimeframe": "This will be the actual price beginning December 01, 2023",
        "LastUpdatedDate": "May 25, 2023"
      }
    ],
    "suppliers": null,
    "brokers": null
  }
]
```

### Rates

---

#### Rates Query

This endpoint can be accessed by the base URL (described above) plus `/Rates`

This endpoint requires a query be provided and the query string has two inputs

1. `id` - The distributor id matching the homeowner's distributor for their area. This can be found by using the [/ZipSearch](#zipsearch) endpoint.
2. `servicetype` - The type of service that you are searching for, for our purposes we will hardcode "residential".
3. `ratetype` - The rate schedule type to search against. Each homeowner should have this predefined for them and can be found "just above the charges on [their] bill".
   - **Note:** A list of possible rate types can be found via the [/ZipSearch](#zipsearch) endpoint within the distributor object.
   - **Note2:** It is also important to note that the rate type selected from the [/ZipSearch](#zipsearch) endpoint should have all spaces replaces by the "+" character.

Valid request example:

```http
www.papowerswitch.com/umbraco/Api/ShopApi/Rates?id=27487&servicetype=residential&ratetype=RH+-+Residential+Heating+Service
```

#### Rates Response Example

200 - OK

```json
[
  {
    "id": 28303,
    "Website": "https://www.aepenergy.com/residential/rates-plans/?utm_source=papower&utm_medium=shopping&utm_campaign=logo",
    "Name": "AEP Energy",
    "LastUpdated": "March 30, 2023",
    "TimeOfUse": {
      "events": [],
      "avgHourly": 1
    },
    "Phone": "1-877-648-1923 ",
    "PriceStructure": "fixed",
    "DiscountAvailable": true,
    "IntroductoryPrice": false,
    "RenewableEnergy": false,
    "CancellationFee": "",
    "TermLength": "24",
    "MonthlyFee": false,
    "MonthlyFeeAmount": "",
    "NetMetering": false,
    "TermEndDate": "NO",
    "TermEndDateInt": 0,
    "EnrollmentFee": false,
    "Rate": 0.1079,
    "UnlimitedRate": 0.0,
    "SignUpLink": "https://www.aepenergy.com/acquisition/campaign/offers/?cc=papower-duq&utm_source=papower&utm_medium=shopping&utm_campaign=duq_24",
    "AllOffersLink": "https://www.aepenergy.com/acquisition/campaign/offers/?cc=papower-duq&utm_source=papower&utm_medium=shopping&utm_campaign=duq_24",
    "MoreInfo": "Enroll in this price plan and you’ll receive up to $120 Reward Dollars to use in AEP Energy Reward Store, our one-stop online marketplace filled with a variety of energy-saving products for your home, available exclusively for AEP Energy customers!  Offer is valid for both new and existing customers. For more information, visit AEPenergyrewardstore.com.",
    "RenewablePercentage": 0.0,
    "PAWind": false,
    "RenewablePA": false,
    "Solar": false
  }
]
```
