from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HairSaloon.bookings'

    def ready(self) -> None:
        import HairSaloon.bookings.signals
