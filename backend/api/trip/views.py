from rest_framework import viewsets

from api.trip.models import Trip
from api.trip.serializers import TripSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
