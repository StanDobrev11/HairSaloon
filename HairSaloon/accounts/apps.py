from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HairSaloon.accounts'

    def ready(self) -> None:
        import HairSaloon.accounts.signals
