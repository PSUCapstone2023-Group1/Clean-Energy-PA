from django.apps import AppConfig


class EmailschedulerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "EmailScheduler"

    def ready(self) -> None:
        from price_watch import price_updater

        price_updater.start()
        return super().ready()
