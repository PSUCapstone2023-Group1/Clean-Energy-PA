from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from price_watch import price_watchdog


def start():
    scheduler = BackgroundScheduler()
    Price_Watch_Dog_Instance = price_watchdog.Price_Watch_Dog()
    scheduler.add_job(Price_Watch_Dog_Instance.check_user_rates, "interval", seconds=5)
    scheduler.start()
