from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

from api.trip.models import Trip


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
    category = models.IntegerField(blank=True, choices=ExpenseCategory.choices)
    date = models.DateTimeField(default=timezone.now)

    @property
    def user(self) -> User:
        return self.trip.user

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["-date"])]
