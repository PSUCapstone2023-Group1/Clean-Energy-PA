from UserRegistration.tests.test_base_view import BaseTest


# Create your tests here.
class GreenEnergySearchBaseTest(BaseTest):
    def setUp(self):
        # Setup the BaseTest first
        super().setUp()
        
        # urls
        self.zipsearch_name = "green_energy_search:zip_search"
        self.rate_type_name = "green_energy_search:rate_type"
        self.offersearch_name = "green_energy_search:offer_search"
