from django.conf import settings

from api.user.email import BaseEmailMessage


class PurchaseSubscriptionNotification(BaseEmailMessage):
    template_name = settings.PURCHASE_SUBSCRIPTION_NOTIFICATION_EMAIL_TEMPLATE
    email_subject = settings.PURCHASE_SUBSCRIPTION_NOTIFICATION_EMAIL_SUBJECT

    def __init__(self, context=None, *args, **kwargs):
        super().__init__(context, *args, **kwargs)
        purchase_failed = self.context.get("purchase_failed", None)
        if purchase_failed:
            self.email_subject = "TravelBalance purchase subscription - FAILED"
        else:
            self.email_subject = "TravelBalance purchase subscription - PASSED"
