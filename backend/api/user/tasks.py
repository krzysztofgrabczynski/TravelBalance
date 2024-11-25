from celery import shared_task
from django.contrib.auth import get_user_model

from api.user.email import (
    ActivationEmail,
    ForgotPasswordEmail,
    FeedbackSendNotification,
)


User = get_user_model()


@shared_task(name="send_activation_user_email_task")
def send_activation_user_email_task(context: dict):
    user_id = context.pop("user_id")
    user = User.objects.get(pk=user_id)
    context.update({"user": user})
    email = ActivationEmail(context=context)
    email.send()


@shared_task(name="send_forgot_password_email_task")
def send_forgot_password_email_task(context: dict):
    email = ForgotPasswordEmail(context=context)
    email.send()


@shared_task(name="send_feedback_notification")
def send_feedback_notification(context: dict):
    email = FeedbackSendNotification(context=context)
    email.send()
