from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from EmailScheduler.contract_watch.contract_watchdog_instance import (
    Contract_Watch_Dog_Instance,
)


def start():
    scheduler = BackgroundScheduler()
    # Checks for rates every 1 day
    # Rates are checked more frequently than emails are sent
    scheduler.add_job(
        Contract_Watch_Dog_Instance.check_contract_end_dates_df,
        id="check_contract_end_dates_df",
        trigger="interval",
        days=1,
    )
    scheduler.start()
