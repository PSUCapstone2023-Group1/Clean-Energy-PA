class rate_response:
    def __init__(self, rate_json):
        self.empty = None
        self.renewable_energy = rate_json["RenewableEnergy"] 
        self.renewable_percentage = rate_json["RenewablePercentage"]        
        self.price_structure = rate_json["PriceStructure"]
        self.monthly_feed = rate_json["MonthlyFeed"]
        self.monthly_fee_amount = rate_json["MonthlyFeeAmount"]       
        self.cancellation_fee = rate_json["CancellationFee"]        
        self.enrollment_fee = rate_json["EnrollmentFee"]
        self.rate = rate_json["Rate"] 