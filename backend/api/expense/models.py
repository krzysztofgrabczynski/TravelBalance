from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from api.trip.models import Trip


class Expense(models.Model):
    class ExpenseCategory(models.IntegerChoices):
        ACCOMODATION = 0
        FOOD = 1
        HEALTH = 2
        TRANSPORT = 3
        ACTIVITIES = 4
        OTHERS = 5

    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name="expenses"
    )
    title = models.CharField(max_length=32)
    cost = models.FloatField(validators=[MinValueValidator(0)])
    category = models.IntegerField(blank=True, choices=ExpenseCategory.choices)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def user(self) -> User:
        return self.trip.user

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["-date"])]
