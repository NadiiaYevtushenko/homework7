from django.apps import AppConfig
import logging

logger = logging.getLogger('django')


class Chat(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        import chat.signals