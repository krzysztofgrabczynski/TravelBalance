from rest_framework import serializers

from api.currency.models import CurrencyRates


class CurrencyRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyRates
        fields = ("date", "rates")
