from django.db import models
from django.contrib.auth.models import User
import uuid


def _user_directory_path(instance, filename):
    return f"trip_images/user_{instance.user.id}/{uuid.uuid4()}_{filename}"


class Trip(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="trips"
    )
    name = models.CharField(max_length=64, blank=False)
    image = models.ImageField(
        upload_to=_user_directory_path,
        default="trip_images/default/default_trip_image.png",
    )
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
