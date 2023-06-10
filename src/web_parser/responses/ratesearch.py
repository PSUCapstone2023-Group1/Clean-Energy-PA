class ratesearch_response:
    # TODO: make this more robust to invalid responses
    def __init__(self, rate_json):
        self.id = str(rate_json["id"])
        self.website = str(rate_json["Website"])
        self.name = str(rate_json["Name"])
        self.renewable_energy = bool(rate_json["RenewableEnergy"])
        self.renewable_percentage = float(rate_json["RenewablePercentage"])
        self.price_structure = str(rate_json["PriceStructure"])
        self.monthly_fee = bool(rate_json["MonthlyFee"])
        self.monthly_fee_amount = str(rate_json["MonthlyFeeAmount"])
        self.cancellation_fee = str(rate_json["CancellationFee"])
        self.enrollment_fee = bool(rate_json["EnrollmentFee"])
        self.rate = float(rate_json["Rate"])
        self.singup_link = str(rate_json["SignUpLink"])
        
    def __str__(self):
        return self.id + ': ' + self.name
        
    def default_filter(self, peco_rate: float):
        return self.renewable_energy == True and \
            self.renewable_percentage == 100 and \
            self.price_structure == "fixed" and \
            self.monthly_fee == False and \
            self.monthly_fee_amount == "" and \
            self.cancellation_fee == "" and \
            self.enrollment_fee == False and \
            self.rate < peco_rate # need to dynamically get that PECO rate still
            
