from rest_framework import serializers

from api.trip.models import Trip


class TripSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Trip
        fields = ["user", "name", "image"]
