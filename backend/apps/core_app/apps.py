from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'apps.core_app'

    def ready(self):
        import apps.core_app.signals
