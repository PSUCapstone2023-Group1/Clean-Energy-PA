from django.apps import AppConfig


class EmailschedulerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "EmailScheduler"

    def ready(self) -> None:
        from EmailScheduler.contract_watch import contract_updater
        from EmailScheduler.price_watch import price_updater
        from EmailScheduler.send_email_batch import email_batch_updater

        # Uncomment to run jobs
        price_updater.start()
        email_batch_updater.start()
        # TODO: Last_Updated (which is used for contract_updater)
        # does not represent term_end_date
        # Need to add another attribute to user_pref for contract_end
        # And a means for user to update
        # contract_updater.start()
        return super().ready()
