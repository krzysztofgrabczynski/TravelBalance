from celery import shared_task
from django.contrib.auth import get_user_model

from api.subscription.email import PurchaseSubscriptionNotification


User = get_user_model()


@shared_task(name="send_purchase_subscription_notification")
def send_purchase_subscription_notification(context: dict):
    if "user_id" in context:
        user_id = context.pop("user_id")
        user = User.objects.get(pk=user_id)
        context.update({"user": user})
    email = PurchaseSubscriptionNotification(context=context)
    email.send()
