from rest_framework import serializers
from datetime import date as datetime_date

from api.trip.models import Trip, Country
from api.expense.serializers import ExpenseSerializerWithoutDetails
from api.currency.currencies_rates_services import get_currency_rates_per_date
from api.currency.serializers import CurrencyRatesSerializer


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class TripReadSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    expenses = ExpenseSerializerWithoutDetails(many=True)
    countries = CountrySerializer(many=True)
    currencies_rates = CurrencyRatesSerializer()

    class Meta:
        model = Trip
        fields = [
            "id",
            "user_detail",
            "name",
            "image_id",
            "countries",
            "date",
            "expenses",
            "currencies_rates",
        ]
        extra_kwargs = {"id": {"read_only": True}}

    def get_user_detail(self, obj: Trip) -> dict:
        return {
            "user_id": obj.user.id,
            "username": obj.user.username,
            "base_currency": obj.user.base_currency,
        }


class TripWriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Trip
        fields = ["id", "user", "name", "image_id", "countries", "date"]
        extra_kwargs = {"id": {"read_only": True}}

    def create(self, validated_data):
        date = datetime_date.today()
        currencies_rates = get_currency_rates_per_date(date)
        validated_data["currencies_rates"] = currencies_rates
        return super().create(validated_data)
