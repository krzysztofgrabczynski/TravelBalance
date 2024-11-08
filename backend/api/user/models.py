from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from random import randint
from uuid import uuid4


class MyUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    base_currency = models.CharField(max_length=3, default="USD")


User = get_user_model()


class ForgotPasswordToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=5)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"ForgotPasswordToken, user - {self.user}"

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = "".join([str(randint(0, 9)) for _ in range(5)])
        return super().save(*args, **kwargs)


class FeedbackFromUser(models.Model):
    class FeedbackType(models.TextChoices):
        ISSUE = "Issue"
        SUGGESTION = "Suggestion"
        OTHER = "Other"

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.TextField(max_length=200, blank=False)
    type = models.CharField(
        max_length=10, choices=FeedbackType.choices, blank=False
    )
    created_date = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user.username} - {self.type}"
