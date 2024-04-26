from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models import signals


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
