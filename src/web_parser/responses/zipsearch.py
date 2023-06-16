from datetime import datetime

class zipsearch_response:
    "A dataclass used to define the structure of the zipsearch object"
    def __init__(self, zipsearch_json):
        self.id = str(zipsearch_json["id"])
        """The distributor's ID"""
        self.name = str(zipsearch_json["Name"])
        """The name of the distributor"""
        self.phone = str(zipsearch_json["Phone"])
        """The distributor's phone number"""
        self.website = str(zipsearch_json["Website"])
        """The distributor's website url"""
        self.rates = list(map(lambda x: zipsearch_rate(x), zipsearch_json["Rates"]))
        """List of rate types for this distributor"""
    
    def __str__(self):
        return self.id + ': ' + self.name

class zipsearch_rate:
    "A dataclass used to define the structure of the zipsearch's rate object"
    def __init__(self, zipsearch_rate_json):
        self.id = str(zipsearch_rate_json["id"])
        """ID of a distributor's rate"""
        self.rate_schedule = str(zipsearch_rate_json["RateSchedule"])
        """The rate schedule definition for this rate type"""
        self.rate = float(zipsearch_rate_json["Rate"])
        """The rate price for this rate type"""
        self.past_rates = list(map(lambda x: zipsearch_past_rate(x), zipsearch_rate_json["PastRates"]))
        """A list of past rates"""
        self.future_rate = float(zipsearch_rate_json["FutureRate"])
        """A known upcoming rate"""
        self.future_rate_timeframe = str(zipsearch_rate_json["FutureRateTimeframe"])
        """A description of when they expect to make the future rate available"""
        self.last_updated_date = str(zipsearch_rate_json["LastUpdatedDate"])
        """The date the rate was last updated, "MMM dd, yyyy" format"""

    def __str__(self):
        return self.id
    
class zipsearch_past_rate:
    "A dataclass used to define the structure of the past_rate object"    

    def __init__(self, past_rate_json):
        self.key = str(past_rate_json["Key"])
        """The datetime that the rate was valid, "yyyy-mm-dd" format"""
        self.value = float(past_rate_json["Value"])
        """The value of the rate"""
        