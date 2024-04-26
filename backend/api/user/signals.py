from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import signals


User = get_user_model()


@receiver(signals.post_save, sender=User)
def send_activation_email_post_save(sender, instance, created, **kwargs):
    if created:
        print("Send email to %s" % instance.username)
    else:
        print("%s just saved" % instance.username)


@receiver(signals.post_save, sender=User)
def set_user_inactive_post_save(sender, instance, created, **kwargs):
    if created:
        instance.is_active = False
        instance.save()
