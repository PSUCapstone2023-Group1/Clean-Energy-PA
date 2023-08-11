from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from EmailScheduler.send_email_batch import email_batch


def start():
    scheduler = BackgroundScheduler()
    Email_Batch_Instance = email_batch.Email_Batch()
    # Send an updated email every week
    scheduler.add_job(
        Email_Batch_Instance.send_lower_rate_emails,
        id="send_lower_rate_emails",
        trigger="interval",
        seconds=30,
    )

    scheduler.add_job(
        Email_Batch_Instance.send_contract_expiration_emails,
        id="send_contract_expiration_emails",
        trigger="interval",
        seconds=30,
    )

    scheduler.start()
