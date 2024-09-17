from django.apps import AppConfig


class MasktConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maskt'

    def ready(self):
        import maskt.signals
