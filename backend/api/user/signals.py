from django.dispatch import receiver, Signal
from django.contrib.auth.models import User
from django.db.models import signals
from api.user.email import ActivationEmail


@receiver(signals.post_save, sender=User)
def set_user_inactive_post_save(sender, instance, created, **kwargs):
    """
    Signal for setting user account as inactive after registration (admin accounts not included).
    """
    if created and not (instance.is_staff or instance.is_superuser):
        instance.is_active = False
        instance.save()
