from rest_framework import serializers

from api.trip.models import Trip, Country
from api.expense.serializers import ExpenseSerializerWithoutDetails


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class TripReadSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    trip_cost = serializers.SerializerMethodField()
    expenses = ExpenseSerializerWithoutDetails(many=True)
    countries = CountrySerializer(many=True)

    class Meta:
        model = Trip
        fields = [
            "id",
            "user_detail",
            "name",
            "image_id",
            "countries",
            "trip_cost",
            "expenses",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_user_detail(self, obj: Trip) -> dict:
        return {"user_id": obj.user.id, "username": obj.user.username}

    def get_trip_cost(self, obj: Trip) -> float | int:
        try:
            return (
                obj.total_cost
            )  # total cost from `TripViewSet.get_queryset` annotate for list action
        except:
            return (
                obj.trip_cost
            )  # trip cost from Trip model property `Trip.trip_cost` for retrieve action


class TripWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Trip
        fields = ["id", "user", "name", "image_id", "countries"]
        extra_kwargs = {"id": {"read_only": True}}
