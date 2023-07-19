from EmailScheduler.tests.test_price_watch_dog import PriceWatchDogTestCase
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance
from django.template.loader import render_to_string
from ..send_email_batch import email_batch
from unittest.mock import Mock, patch
from django.conf import settings
from django.core.mail import outbox


class PriceWatchDogTestCase(PriceWatchDogTestCase):
    def setUp(self):
        super().setUp()

    def test_send_lower_rate_emails(self):
        email_batch_instance = email_batch.Email_Batch()
        email_batch_instance.send_lower_rate_emails()
        self.assertTrue(email_batch_instance.send_email_return)
