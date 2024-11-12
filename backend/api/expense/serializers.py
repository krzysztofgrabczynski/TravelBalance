from rest_framework import serializers

from api.expense.models import Expense
from api.currency.currencies_rates_services import (
    convert_currency,
)


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
            "cost_per_base_currency",
            "category",
            "date",
            "currency",
            "trip_detail",
            "user_detail",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "trip": {"read_only": True},
            "cost_per_base_currency": {"read_only": True},
        }

    def get_trip_detail(self, obj: Expense) -> dict:
        return {"trip_id": obj.trip.id, "trip_name": obj.trip.name}

    def get_user_detail(self, obj: Expense) -> dict:
        return {
            "user_id": obj.trip.user.id,
            "username": obj.trip.user.username,
        }

    def create(self, validated_data: dict) -> Expense:
        validated_data["cost_per_base_currency"] = validated_data["cost"]
        expense = super().create(validated_data)
        converted_cost = self._get_converted_cost_to_base_currency(expense)
        if converted_cost:
            expense.cost_per_base_currency = converted_cost
            expense.save()
        return expense

    def update(self, instance: Expense, validated_data: dict) -> Expense:
        validated_data["cost_per_base_currency"] = validated_data["cost"]
        expense = super().update(instance, validated_data)
        converted_cost = self._get_converted_cost_to_base_currency(expense)
        if converted_cost:
            expense.cost_per_base_currency = converted_cost
            expense.save()
        return expense

    def _get_converted_cost_to_base_currency(
        self, expense: Expense
    ) -> None | float:
        """
        If user's base currency is diffrent than currency from request, `cost_per_base_currency` field is converted from base currency.
        """

        base_currency = expense.trip.user.base_currency
        source_currency = expense.currency

        if base_currency != expense.currency:
            currencies_rates = expense.trip.currencies_rates.rates

            amount_source_currency = expense.cost
            rate_source_to_USD = currencies_rates[source_currency]
            rate_targed_to_USD = currencies_rates[base_currency]

            return convert_currency(
                amount_source_currency,
                rate_source_to_USD,
                rate_targed_to_USD,
            )


class ExpenseSerializerWithoutDetails(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "title",
            "cost",
            "cost_per_base_currency",
            "category",
            "date",
            "currency",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "cost_per_base_currency": {"read_only": True},
        }
