from rest_framework import serializers

from api.trip.models import Trip
from api.expense.serializers import ExpenseSerializer



class TripSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    trip_cost = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ["id", "user", "name", "image", "trip_cost"]
        extra_kwargs = {"id": {"read_only": True}}

    def get_trip_cost(self, obj: Trip) -> float | int:
        return obj.trip_cost

class TripWithExpensesSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    trip_cost = serializers.SerializerMethodField()
    expenses = ExpenseSerializer(many=True)

    class Meta:
        model = Trip
        fields = ["id", "user", "name", "image", "trip_cost", "expenses"]
        extra_kwargs = {"id": {"read_only": True}}

    def get_trip_cost(self, obj: Trip) -> float | int:
            return obj.trip_cost


