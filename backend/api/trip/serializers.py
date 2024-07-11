from rest_framework import serializers

from api.trip.models import Trip
from api.expense.serializers import ExpenseSerializerWithoutDetails


class TripBaseSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user_detail = serializers.SerializerMethodField()
    trip_cost = serializers.SerializerMethodField()

    def get_user_detail(self, obj: Trip) -> dict:
        return {"user_id": obj.user.id, "username": obj.user.username}

    def get_trip_cost(self, obj: Trip) -> float | int:
        return obj.trip_cost


class TripSerializer(TripBaseSerializer, serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ["id", "user", "user_detail", "name", "image", "trip_cost"]
        extra_kwargs = {"id": {"read_only": True}}


class TripWithExpensesSerializer(
    TripBaseSerializer, serializers.ModelSerializer
):
    expenses = ExpenseSerializerWithoutDetails(many=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "user",
            "user_detail",
            "name",
            "image",
            "trip_cost",
            "expenses",
        ]
        extra_kwargs = {"id": {"read_only": True}}
