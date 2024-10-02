from django.db import models
from django.contrib.auth.models import User
import uuid


def _user_directory_path(instance, filename):
    return f"trip_images/user_{instance.user.id}/{uuid.uuid4()}_{filename}"


class Country(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Countries"


class Image(models.Model):
    image = models.ImageField(upload_to="trip_images/")
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["id"]


class Trip(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="trips"
    )
    name = models.CharField(max_length=64, blank=False)
    image = models.ForeignKey(
        Image, on_delete=models.SET_NULL, null=True, blank=True
    )
    countries = models.ManyToManyField(Country, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def trip_cost(self) -> int:
        aggregate_dict = self.expenses.aggregate(total_cost=models.Sum("cost"))
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
