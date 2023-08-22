from django.apps import AppConfig


class YourAppNameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "library"

    def ready(self):
        import library.signals
