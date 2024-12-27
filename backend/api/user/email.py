from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured

from core import settings


class BaseEmailMessage(EmailMultiAlternatives):
    template_name = None
    email_subject = None

    def __init__(self, context: dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context = {} if context is None else context

    def set_context_data(self) -> None:
        protocol = self.context.get("protocol") or "https"
        domain = self.context.get("domain") or settings.DOMAIN_NAME
        self.context.update({"protocol": protocol, "domain": domain})

        subject = self.context.get("subject") or self.email_subject
        from_email = self.context.get("from_email") or settings.DEFAULT_EMAIL
        to = self.context.get("to") or []
        cc = self.context.get("cc") or []
        bcc = self.context.get("bcc") or []

        self.context.update(
            {
                "subject": subject,
                "from_email": from_email,
                "to": to if isinstance(to, list) else [to],
                "cc": cc if isinstance(cc, list) else [cc],
                "bcc": bcc if isinstance(bcc, list) else [bcc],
            }
        )

    def send(self, fail_silently: bool = False) -> int:
        self.set_context_data()

        html_content = render_to_string(self.get_template_name(), self.context)
        self.body = strip_tags(html_content)
        self.attach_alternative(html_content, "text/html")

        self.subject = self.context["subject"]
        self.from_email = self.context["from_email"]
        self.to = self.context["to"]
        self.cc = self.context["cc"]
        self.bcc = self.context["bcc"]

        return super().send(fail_silently)

    def get_template_name(self) -> str:
        if self.template_name is None:
            error_message = f"The `template_name` attribute in the {self.__class__.__name__} class cannot be None."
            raise ImproperlyConfigured(error_message)
        return self.template_name


class ActivationEmail(BaseEmailMessage):
    template_name = settings.ACTIVATION_EMAIL_TEMPLATE
    email_subject = settings.ACTIVATION_EMAIL_SUBJECT

    def set_context_data(self) -> None:
        super().set_context_data()

        user = self.context["user"]
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = self.context.get(
            "token"
        ) or default_token_generator.make_token(user)
        url = reverse(
            "user-account_activation",
            kwargs={"uidb64": uidb64, "token": token},
        )

        self.context.update({"uidb64": uidb64, "token": token, "url": url})


class ForgotPasswordEmail(BaseEmailMessage):
    template_name = settings.FORGOT_PASSWORD_EMAIL_TEMPLATE
    email_subject = settings.FORGOT_PASSWORD_EMAIL_SUBJECT


class FeedbackSendNotification(BaseEmailMessage):
    template_name = settings.FEEDBACK_SEND_NOTIFICATION_EMAIL_TEMPLATE
    email_subject = settings.FEEDBACK_SEND_NOTIFICATION_EMAIL_SUBJECT

    def __init__(self, context=None, *args, **kwargs):
        super().__init__(context, *args, **kwargs)
        feedback_type = self.context.get("feedback_type")
        if feedback_type:
            self.email_subject = f"Feedback semd from TravelBalance application - {feedback_type}"
