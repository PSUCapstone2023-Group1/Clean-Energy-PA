expected_example = [
    {
        "id": 28734,
        "Website": "https://energypricing.com",
        "Name": "Achieve Energy Solutions LLC DBA EnergyPricing.com",
        "LastUpdated": "June 03, 2023",
        "TimeOfUse": {"events": []},
        "Phone": "1-800-225-3813",
        "PriceStructure": "fixed",
        "DiscountAvailable": True,
        "IntroductoryPrice": False,
        "RenewableEnergy": False,
        "CancellationFee": "",
        "TermLength": "17",
        "MonthlyFee": False,
        "MonthlyFeeAmount": "",
        "NetMetering": False,
        "TermEndDate": "NO",
        "TermEndDateInt": 0,
        "EnrollmentFee": False,
        "Rate": 0.0839,
        "UnlimitedRate": 0.0,
        "SignUpLink": "https://energypricing.com/enrollmentrequest/?plan=7597",
        "AllOffersLink": "https://energypricing.com/shop/electric-rates.html?customer_type=6&plan_product_type=8&plan_state=51&utility=96",
        "MoreInfo": "Achieve Energy Solutions, LLC d/b/a EnergyPricing.com is a licensed electricity broker representing other suppliers. \nPrices listed are subject to change without notice.  \nFinal prices, terms and conditions will be reflected in supplier agreements.",
        "RenewablePercentage": 0.0,
        "PAWind": False,
        "RenewablePA": False,
        "Solar": False,
    },
    {
        "id": 28735,
        "Website": "https://energypricing.com",
        "Name": "Achieve Energy Solutions LLC DBA EnergyPricing.com",
        "LastUpdated": "June 03, 2023",
        "TimeOfUse": {"events": []},
        "Phone": "1-800-225-3813",
        "PriceStructure": "fixed",
        "DiscountAvailable": False,
        "IntroductoryPrice": False,
        "RenewableEnergy": True,
        "CancellationFee": "",
        "TermLength": "17",
        "MonthlyFee": False,
        "MonthlyFeeAmount": "",
        "NetMetering": False,
        "TermEndDate": "NO",
        "TermEndDateInt": 0,
        "EnrollmentFee": False,
        "Rate": 0.0839,
        "UnlimitedRate": 0.0,
        "SignUpLink": "https://energypricing.com/enrollmentrequest/?plan=7597",
        "AllOffersLink": "https://energypricing.com/shop/electric-rates.html?customer_type=6&plan_product_type=8&plan_state=51&utility=96",
        "MoreInfo": "Achieve Energy Solutions, LLC d/b/a EnergyPricing.com is a licensed electricity broker representing other suppliers. \nPrices listed are subject to change without notice.  \nFinal prices, terms and conditions will be reflected in supplier agreements.",
        "RenewablePercentage": 100,
        "PAWind": False,
        "RenewablePA": False,
        "Solar": False,
    },
]
unexpected_example = [
    {
        "id": 28734,
        "Website": "https://energypricing.com",
        "Name": "Achieve Energy Solutions LLC DBA EnergyPricing.com",
        "LastUpdated": "June 03, 2023",
        "TimeOfUse": {"events": []},
        "Phone": "1-800-225-3813",
        "PriceStructure": "fixed",
        "DiscountAvailable": False,
        "IntroductoryPrice": False,
        "RenewableEnergy": False,
        "CancellationFee": "",
        "TermLength": "17",
        "MonthlyFee": False,
        "MonthlyFeeAmount": "",
        "NetMetering": False,
        "TermEndDate": "NO",
        "TermEndDateInt": 0,
        "EnrollmentFee": False,
        "Rate": "abcd",  #! bad rate format given
        "UnlimitedRate": 0.0,
        "SignUpLink": "https://energypricing.com/enrollmentrequest/?plan=7597",
        "AllOffersLink": "https://energypricing.com/shop/electric-rates.html?customer_type=6&plan_product_type=8&plan_state=51&utility=96",
        "MoreInfo": "Achieve Energy Solutions, LLC d/b/a EnergyPricing.com is a licensed electricity broker representing other suppliers. \nPrices listed are subject to change without notice.  \nFinal prices, terms and conditions will be reflected in supplier agreements.",
        "RenewablePercentage": 0.0,
        "PAWind": False,
        "RenewablePA": False,
        "Solar": False,
    }
]
