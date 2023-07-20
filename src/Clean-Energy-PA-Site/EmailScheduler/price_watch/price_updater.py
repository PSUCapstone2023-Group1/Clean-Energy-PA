from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance


def start():
    scheduler = BackgroundScheduler()
    # Checks for rates every 5 days
    scheduler.add_job(
        Price_Watch_Dog_Instance.update_lower_rate_mailing_list_df,
        "interval",
        days=5,
    )
    scheduler.start()
