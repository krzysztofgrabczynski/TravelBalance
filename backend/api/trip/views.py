from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator

from api.trip.models import Trip
from api.trip.serializers import TripSerializer
from api.permissions import ObjectOwnerPermission
from api.subscription_restrictions import add_trip_limit


@method_decorator(add_trip_limit, name="create")
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, ObjectOwnerPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.filter(user=self.request.user)
        return queryset
