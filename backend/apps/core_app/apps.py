from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'apps.core_app'

    def ready(self):
        print('import apps.core_app.signals')
        import apps.core_app.signals
