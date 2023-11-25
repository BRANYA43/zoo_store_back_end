from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=get_user_model())
def user_created(sender, instance, **kwargs):
    if not getattr(instance, 'profile', None):
        Profile.objects.create(user=instance)