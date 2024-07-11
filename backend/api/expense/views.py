from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.expense.models import Expense
from api.trip.models import Trip
from api.expense.serializers import ExpenseSerializer
from api.permissions import TripOwnerPermission, ObjectOwnerPermission


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [
        IsAuthenticated,
        TripOwnerPermission,
        ObjectOwnerPermission,
    ]
    trip_lookup_field = "trip_pk"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            trip_pk = self.kwargs.get(self.trip_lookup_field)
            return queryset.filter(trip_id=trip_pk)
        return queryset

    def perform_create(self, serializer):
        self._perform_save_with_trip_obj(serializer)

    def perform_update(self, serializer):
        self._perform_save_with_trip_obj(serializer)

    def _perform_save_with_trip_obj(self, serializer):
        trip_pk = self.kwargs.get(self.trip_lookup_field)
        trip = Trip.objects.get(pk=trip_pk)
        serializer.save(trip=trip)
