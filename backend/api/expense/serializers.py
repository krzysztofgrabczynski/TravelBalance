from rest_framework import serializers

from api.expense.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    trip_detail = serializers.SerializerMethodField()
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = [
            "id",
            "trip",
            "title",
            "cost",
            "category",
            "date",
            "trip_detail",
            "user_detail",
        ]
        extra_kwargs = {"id": {"read_only": True}, "trip": {"read_only": True}}

    def get_trip_detail(self, obj: Expense) -> dict:
        return {"trip_id": obj.trip.id, "trip_name": obj.trip.name}

    def get_user_detail(self, obj: Expense) -> dict:
        return {
            "user_id": obj.trip.user.id,
            "username": obj.trip.user.username,
        }


class ExpenseSerializerWithoutDetails(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "title", "cost", "category", "date"]
        extra_kwargs = {"id": {"read_only": True}}
