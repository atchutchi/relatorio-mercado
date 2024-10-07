from django.apps import AppConfig


class IndicatorManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indicator_management'

    def ready(self):
        import indicator_management.signals
