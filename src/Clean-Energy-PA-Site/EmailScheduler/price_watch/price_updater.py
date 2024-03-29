from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from EmailScheduler.price_watch.price_watchdog_instance import Price_Watch_Dog_Instance


def start():
    scheduler = BackgroundScheduler()
    # Checks for rates every 1 day
    # Rates are checked more frequently than emails are sent
    scheduler.add_job(
        Price_Watch_Dog_Instance.update_lower_rate_mailing_list_df,
        id="update_lower_rate_mailing_list_df",
        trigger="interval",
        days=1,
    )
    scheduler.start()
