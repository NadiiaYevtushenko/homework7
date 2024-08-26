from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserStatus

@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': True})

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    UserStatus.objects.update_or_create(user=user, defaults={'is_online': False})
