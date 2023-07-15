from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from price_watch import price_watchdog


def start():
    pass  # passing to avoid running in production while testing
    # scheduler = BackgroundScheduler()
    # Price_Watch_Dog_Instance = price_watchdog.Price_Watch_Dog()
    # scheduler.add_job(
    #     Price_Watch_Dog_Instance.update_mailing_list_df, "interval", seconds=5
    # )
    # scheduler.start()
