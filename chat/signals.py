import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Message)
def log_message(sender, instance, created, **kwargs):
    if created:
        log_msg = f"Message from {instance.sender} to {instance.recipient} at {instance.timestamp}"
        logger.debug(log_msg)

        if instance.recipient.is_superuser:
            instance.send_success_to_sender = True
            instance.save()