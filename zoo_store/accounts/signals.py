from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def created_user(sender, instance, *args, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
