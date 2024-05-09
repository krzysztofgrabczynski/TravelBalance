from django.db import models
from django.contrib.auth.models import User
from random import randint
from uuid import uuid4


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
