from django.conf import settings

from api.user.email import BaseEmailMessage


class FetchCurrencyFailedEmail(BaseEmailMessage):
    template_name = settings.FETCH_CURRENCY_FAILED_EMAIL_TEMPLATE
    email_subject = settings.FETCH_CURRENCY_FAILED_EMAIL_SUBJECT

    def set_context_data(self) -> None:
        super().set_context_data()

        status_code = self.context["status_code"]
        message = self.context["message"]
        self.context.update({"status_code": status_code, "message": message})
