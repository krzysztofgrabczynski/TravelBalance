from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import signals


@receiver(signals.post_save, sender=User)
def send_activation_email_post_save(sender, instance, created, **kwargs):
    """
    Signal for sending email with activation code for activate user account (admin accounts not included).
    """
    if created and not (instance.is_staff or instance.is_superuser):
        print("Send email to %s" % instance.username)
    else:
        print("%s just saved" % instance.username)


@receiver(signals.post_save, sender=User)
def set_user_inactive_post_save(sender, instance, created, **kwargs):
    """
    Signal for setting user account as inactive after registration (admin accounts not included).
    """
    if created and not (instance.is_staff or instance.is_superuser):
        instance.is_active = False
        instance.save()
