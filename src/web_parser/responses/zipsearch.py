class zipsearch_response:
    # TODO: make this more robust to invalid responses
    def __init__(self, zipsearch_json):
        self.id = str(zipsearch_json["id"])
        self.name = str(zipsearch_json["Name"])
        self.phone = str(zipsearch_json["Phone"])
        self.website = str(zipsearch_json["Website"])
        self.rates = list(map(lambda x: zipsearch_rate(x), zipsearch_json["Rates"]))
    
    def __str__(self):
        return self.id + ': ' + self.name

class zipsearch_rate:
    # TODO: make this more robust to invalid responses
    def __init__(self, zipsearch_rate_json):
        self.id = str(zipsearch_rate_json["id"])
        self.rate_schedule = str(zipsearch_rate_json["RateSchedule"])
        self.rate = float(zipsearch_rate_json["Rate"])
        self.future_rate = float(zipsearch_rate_json["FutureRate"])
        self.future_rate_timeframe = str(zipsearch_rate_json["FutureRateTimeframe"])
        self.last_updated_date = str(zipsearch_rate_json["LastUpdatedDate"])

    def __str__(self):
        return self.id