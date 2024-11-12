from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from api.user.models import MyUser
from django.utils import timezone

from api.trip.models import Trip


User = get_user_model()


class Expense(models.Model):
    class ExpenseCategory(models.IntegerChoices):
        ACTIVITIES = 0
        ACCOMODATION = 1
        FOOD = 2
        HEALTH = 3
        SHOPPING = 4
        TRANSPORT = 5
        SOUVENIRS = 6
        OTHERS = 7

    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="expenses"
    )
    title = models.CharField(max_length=32, default="")
    cost = models.FloatField(validators=[MinValueValidator(0.01)])
    cost_per_base_currency = models.FloatField()
    category = models.IntegerField(blank=True, choices=ExpenseCategory.choices)
    date = models.DateTimeField(default=timezone.now)
    currency = models.CharField(max_length=3)

    @property
    def user(self) -> MyUser:
        return self.trip.user

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["-date"])]
