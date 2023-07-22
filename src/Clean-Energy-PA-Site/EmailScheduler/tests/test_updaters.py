from EmailScheduler.tests.test_price_watch_dog import PriceWatchDogTestCase
from EmailScheduler.send_email_batch.email_batch_updater import (
    start as email_batch_start,
)
from EmailScheduler.price_watch.price_updater import start as price_watch_start
from EmailScheduler.contract_watch.contract_updater import start as contract_watch_start
from unittest.mock import patch


class UpdatersTestCase(PriceWatchDogTestCase):
    def setUp(self):
        super().setUp()

    @patch("EmailScheduler.send_email_batch.email_batch_updater.BackgroundScheduler")
    def test_email_batch_updater(self, mock_scheduler):
        email_batch_start()
        mock_scheduler.assert_called_once()

    @patch("EmailScheduler.price_watch.price_updater.BackgroundScheduler")
    def test_price_updater(self, mock_scheduler):
        price_watch_start()
        mock_scheduler.assert_called_once()

    @patch("EmailScheduler.contract_watch.contract_updater.BackgroundScheduler")
    def test_contract_updater(self, mock_scheduler):
        contract_watch_start()
        mock_scheduler.assert_called_once()
