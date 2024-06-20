from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.trip.models import Trip
from api.trip.serializers import TripSerializer
from api.permissions import ObjectOwnerPermission


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, ObjectOwnerPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.filter(user=self.request.user)
        return queryset
