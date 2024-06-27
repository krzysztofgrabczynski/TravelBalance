from rest_framework import serializers

from api.expense.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "trip", "title", "cost", "category", "data"]
        extra_kwargs = {"id": {"read_only": True}}
