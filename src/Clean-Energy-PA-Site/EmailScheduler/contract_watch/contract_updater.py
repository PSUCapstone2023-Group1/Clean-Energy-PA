from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from EmailScheduler.contract_watch.contract_watchdog_instance import (
    Contract_Watch_Dog_Instance,
)


def start():
    scheduler = BackgroundScheduler()
    # Check contracts daily
    scheduler.add_job(
        Contract_Watch_Dog_Instance.check_contract_end_dates_df,
        id="check_contract_end_dates_df",
        trigger="interval",
        seconds=30,
    )
    scheduler.start()
