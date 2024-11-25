from django.conf import settings

from api.user.email import BaseEmailMessage


class FetchCurrencyFailedEmail(BaseEmailMessage):
    template_name = settings.FETCH_CURRENCY_FAILED_EMAIL_TEMPLATE
    email_subject = settings.FETCH_CURRENCY_FAILED_EMAIL_SUBJECT
