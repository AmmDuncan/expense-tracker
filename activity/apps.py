from django.apps import AppConfig


class ActivityConfig(AppConfig):
    name = 'activity'

    def ready(self):
        from . import signals
