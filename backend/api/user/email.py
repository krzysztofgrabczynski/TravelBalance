from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
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

    def __init__(self, request, context=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request
        self.context = {} if context is None else context

    def set_context_data(self) -> None:
        current_site = get_current_site(self.request)

        user = self.context.get("user") or self.request.user
        subject = (
            self.context.get("subject") or settings.ACTIVATION_EMAIL_SUBJECT
        )
        from_email = self.context.get("from_email") or settings.DEFAULT_EMAIL
        to = self.context.get("to") or user.email
        cc = self.context.get("cc") or []
        bcc = self.context.get("bcc") or []

        protocol = self.context.get("protocol") or (
            "https" if self.request.is_secure() else "http"
        )
        domain = self.context.get("domain") or current_site.domain

        self.context.update(
            {
                "user": user,
                "subject": subject,
                "from_email": from_email,
                "to": to if isinstance(to, list) else [to],
                "cc": cc if isinstance(cc, list) else [cc],
                "bcc": bcc if isinstance(bcc, list) else [bcc],
                "protocol": protocol,
                "domain": domain,
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

    def get_template_name(self):
        if self.template_name is None:
            raise ImproperlyConfigured
        return self.template_name


class ActivationEmail(BaseEmailMessage):
    template_name = settings.ACTIVATION_EMAIL_TEMPLATE

    def set_context_data(self) -> None:
        super().set_context_data()

        user = self.context["user"]
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse(
            "user-account_activation",
            kwargs={"uidb64": uidb64, "token": token},
        )

        self.context.update({"uidb64": uidb64, "token": token, "url": url})
