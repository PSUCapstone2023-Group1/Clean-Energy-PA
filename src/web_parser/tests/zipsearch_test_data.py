expected_example=[
  {
    "id": 27498,
    "Name": "PECO Energy",
    "Phone": "1-800-494-4000",
    "Website": "https://www.peco.com/",
    "Rates": [
      {
        "id": 27499,
        "RateSchedule": "R - Regular Residential Service",
        "Rate": 0.10312,
        "PastRates": [
          {
            "Key": "2020-09-01",
            "Value": 0.06405
          }
        ],
        "FutureRate": 0.0,
        "FutureRateTimeframe": "This will be the actual price beginning September 01, 2023",
        "LastUpdatedDate": "May 15, 2023"
      },
      {
        "id": 27500,
        "RateSchedule": "RH - Residential Heating Service",
        "Rate": 0.10312,
        "PastRates": [
          {
            "Key": "2017-09-01",
            "Value": 0.0713
          }
        ],
        "FutureRate": 0.0,
        "FutureRateTimeframe": "This will be the actual price beginning September 01, 2023",
        "LastUpdatedDate": "May 15, 2023"
      }
    ],
    "suppliers": None,
    "brokers": None
  }
]

unexpected_example=[
  {
    "id": 27498, 
    "Name": "PECO Energy",
    "Phone": "1-800-494-4000",
    "Website": "https://www.peco.com/",
    "Rates": [
      {
        "id": 27499,
        "RateSchedule": "R - Regular Residential Service",
        "Rate": "abcd", #! bad rate value
        "PastRates": [
          {
            "Key": "2020-09-01",
            "Value": 0.06405
          }
        ],
        "FutureRate": 0.0,
        "FutureRateTimeframe": "This will be the actual price beginning September 01, 2023",
        "LastUpdatedDate": "May 15, 2023"
      },
      {
        "id": 27500,
        "RateSchedule": "RH - Residential Heating Service",
        "Rate": 0.10312,
        "PastRates": [
          {
            "Key": "2017-09-01",
            "Value": 0.0713
          }
        ],
        "FutureRate": 0.0,
        "FutureRateTimeframe": "This will be the actual price beginning September 01, 2023",
        "LastUpdatedDate": "May 15, 2023"
      }
    ],
    "suppliers": None,
    "brokers": None
  }
]