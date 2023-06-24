from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from GreenEnergySearch.models import User_Preferences


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        # Dummy user data
        self.test_user = User.objects.create_user(
            username="JohnDoe",
            password="TestUserPass1234",
            first_name="John",
            last_name="Doe",
            is_active=True,
        )

        # Dummy user preferences data
        self.test_user_preferences = User_Preferences.objects.create(
            user_id=self.test_user,
            zip_code="15026",
            rate_schedule="rate schedule",
            distributor_id=1234,
            selected_offer_id=5678,
            selected_offer_rate=2.2,
            email_notifications=True,
        )

    def test_login_and_navigate(self):
        # Log in the user
        self.selenium.get(f"{self.live_server_url}/login")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("JohnDoe")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("TestUserPass1234")
        login_button_xpath = (
            '//*[@id="content"]/div/div/div[2]/div/div/form/div[3]/div/button'
        )
        login_button = self.selenium.find_element(By.XPATH, login_button_xpath)
        login_button.click()

        # Wait for the login process to complete
        # Then click the profile icon
        profile_icon_xpath = '//*[@id="navbarNav"]/ul/li[4]/div/a/i'
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.XPATH, profile_icon_xpath))
        )

        # Navigate to the edit_profile page
        self.selenium.get(self.live_server_url + "/edit_profile/")
        time.sleep(10)
        # Assert that the user is on the edit_profile page
        self.assertIn("/edit_profile/", self.selenium.current_url)

        # Wait for a bit to look at the page if desired
        time.sleep(30)
