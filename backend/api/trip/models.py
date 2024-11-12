from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

from api.currency.models import CurrencyRates


User = get_user_model()


def _user_directory_path(instance, filename):
    return f"trip_images/user_{instance.user.id}/{uuid.uuid4()}_{filename}"


class Country(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Trip(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="trips"
    )
    name = models.CharField(max_length=32, blank=False)
    image_id = models.SmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(9)]
    )
    countries = models.ManyToManyField(Country, blank=True)
    date = models.DateTimeField(default=timezone.now)
    created_at = models.DateField(auto_now_add=True)
    currencies_rates = models.ForeignKey(
        CurrencyRates, on_delete=models.DO_NOTHING
    )

    @property
    def trip_cost(self) -> int:
        aggregate_dict = self.expenses.aggregate(
            total_cost=models.Sum("cost_per_base_currency")
        )
        if aggregate_dict.get("total_cost"):
            return round(aggregate_dict.get("total_cost"), 2)
        return 0

    @property
    def expenses_amount(self) -> int:
        return self.expenses.count()

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["-date"])]
