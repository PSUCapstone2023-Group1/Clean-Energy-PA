from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from price_watch import price_watchdog


def start():
    scheduler = BackgroundScheduler()
    dog = price_watchdog.Price_Watch_Dog()
    scheduler.add_job(dog.check_user_rates, "interval", minutes=5)
    scheduler.start()
