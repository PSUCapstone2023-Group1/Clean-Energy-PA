from enum import Enum

class price_structure(Enum):
    """List of the possible price structure options"""
    fixed="fixed"
    variable="variable"
    unlimited="unlimited"

class offer:
    "A dataclass used to define the structure of the ratesearch's offer object"
    def __init__(self, rate_json):
        self.id = str(rate_json["id"])
        """ID of this rate offer"""
        self.website = str(rate_json["Website"])
        """The website of the rate offer provider"""
        self.name = str(rate_json["Name"])
        """The name of the rate offer provider"""
        self.last_updated = str(rate_json["LastUpdated"])
        """The date that this rate offer was last updated, "MMM dd, yyyy" format"""
        self.time_of_use = rate_json["TimeOfUse"]
        """Not sure what this is for"""
        self.phone = rate_json["Phone"]
        """Phone number of the rate offer provider"""
        self.price_structure = str(rate_json["PriceStructure"])
        """The price structure of this offer"""
        self.discount_available = bool(rate_json["DiscountAvailable"])
        """Does this offer have a discount?"""
        self.introductory_price = bool(rate_json["IntroductoryPrice"])
        """Does this offer have an intro price?"""
        self.renewable_energy = bool(rate_json["RenewableEnergy"])
        """Does this offer use renewable energy?"""
        self.cancellation_fee = str(rate_json["CancellationFee"])
        """A description of the cancellation fee"""
        self.term_length = str(rate_json["TermLength"])
        """A description of the term length"""
        self.monthly_fee = bool(rate_json["MonthlyFee"])
        """Does this offer have a monthly fee?"""
        self.monthly_fee_amount = str(rate_json["MonthlyFeeAmount"])
        """A description of the monthly fee amount"""
        self.net_metering = bool(rate_json["NetMetering"])
        """Does this offer use net metering?"""
        self.term_end_date=str(rate_json["TermEndDate"])
        """A description of the term end date"""
        self.term_end_date_int=int(rate_json["TermEndDateInt"])
        """An integer representation of the term end date"""
        self.enrollment_fee = bool(rate_json["EnrollmentFee"])
        """Does this offer have an enrollment fee?"""
        self.rate = float(rate_json["Rate"])
        """The rate that this offer provides"""
        self.unlimited_rate = float(rate_json["UnlimitedRate"])
        """Not sure what this is for"""
        self.singup_link = str(rate_json["SignUpLink"])
        """The url to signup for this offer"""
        self.all_offers_link = str(rate_json["AllOffersLink"])
        """A link to show all offers for this provider"""
        self.more_info = str(rate_json["MoreInfo"])
        """A description that provides more information for this offer"""
        self.renewable_percentage = float(rate_json["RenewablePercentage"])
        """The renewable percentage of this offer"""
        self.pa_wind = bool(rate_json["PAWind"])
        """Does this offer use PA Wind?"""
        self.renewable_pa = bool(rate_json["RenewablePA"])
        """Does this offer partner with renewable PA?"""
        self.solar = bool(rate_json["Solar"])
        """Does this offer use solar energy?"""

    def __str__(self):
        return self.id + ': ' + self.name
    
    def filter(self, #NOSONAR
                name:None|str=None,
                discount_available:None|bool=None,
                net_metering:None|bool=None,
                pa_wind:None|bool=None,
                renewable_pa:None|bool=None,
                solar:None|bool=None,
                introductory_price:None|bool=None,
                renewable_energy:None|bool=None,
                lower_renewable_percentage:None|float=None,
                price_structure:None|price_structure=None,
                monthly_fee:None|bool=None,
                monthly_fee_amount:None|str=None,
                cancellation_fee:None|str=None,
                enrollment_fee:None|bool=None,
                upper_rate:None|float=None
                ):
        """Checks if this offer meets the filter conditions"""
        conditions:list[bool] = [] #initialize the conditions list

        # Only check conditions that are not None.
        if name is not None:
            conditions.append(self.name==name)
        if discount_available is not None:
            conditions.append(self.discount_available==discount_available)
        if pa_wind is not None:
            conditions.append(self.pa_wind==pa_wind)
        if renewable_pa is not None:
            conditions.append(self.renewable_pa==renewable_pa)
        if solar is not None:
            conditions.append(self.solar==solar)
        if introductory_price is not None:
            conditions.append(self.introductory_price==introductory_price)
        if net_metering is not None:
            conditions.append(self.net_metering==net_metering)
        if renewable_energy is not None:
            conditions.append(self.renewable_energy==renewable_energy)
        if lower_renewable_percentage is not None:
            conditions.append(self.renewable_percentage>=lower_renewable_percentage)
        if price_structure is not None:
            conditions.append(self.price_structure==str(price_structure))
        if monthly_fee is not None:
            conditions.append(self.monthly_fee==monthly_fee)
        if monthly_fee_amount is not None:
            conditions.append(self.monthly_fee_amount==monthly_fee_amount)
        if cancellation_fee is not None:
            conditions.append(self.cancellation_fee==cancellation_fee)
        if enrollment_fee is not None:
            conditions.append(self.enrollment_fee==enrollment_fee)
        if upper_rate is not None:
            conditions.append(self.rate<=upper_rate)

        return len(conditions)==0 or all(conditions) # If no filter conditions were requested return true, otherwise verify that all filter conditions are true 
    
class offer_collection:
    """Handler for a collection of offers"""
    collection:list[offer]
    """List of offers in the collection"""
    def __init__(self, offers_json):
        self.collection = list(map(lambda x: offer(x), offers_json))
        self.index=0

    def __getitem__(self, index)->offer:
        return self.collection[index]
    
    def __len__(self):
        return len(self.collection)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.collection):
            item = self.collection[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration()

    def filter(self, #NOSONAR
                name:None|str=None,
                discount_available:None|bool=None,
                net_metering:None|bool=None,
                pa_wind:None|bool=None,
                renewable_pa:None|bool=None,
                solar:None|bool=None,
                introductory_price:None|bool=None,
                renewable_energy:None|bool=None,
                lower_renewable_percentage:None|float=None,
                price_structure:None|price_structure=None,
                monthly_fee:None|bool=None,
                monthly_fee_amount:None|str=None,
                cancellation_fee:None|str=None,
                enrollment_fee:None|bool=None,
                upper_rate:None|float=None):
        "Collection filter which returns a list of only the items where the filter conditions passed"
        return [offer for offer in self if offer.filter(name, 
                                                                discount_available,
                                                                net_metering, pa_wind,
                                                                renewable_pa, solar, 
                                                                introductory_price, 
                                                                renewable_energy,
                                                                lower_renewable_percentage,
                                                                price_structure,
                                                                monthly_fee,
                                                                monthly_fee_amount,
                                                                cancellation_fee,
                                                                enrollment_fee,
                                                                upper_rate)] 
