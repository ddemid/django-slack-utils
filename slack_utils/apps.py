from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class SlackUtilsConfig(AppConfig):
    name = 'slack_utils'
    verbose_name = "Slack Utils"

    def ready(self):
        super().ready()

        autodiscover_modules('slack_events')
