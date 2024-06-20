from rest_framework import viewsets, exceptions
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from api.expense.models import Expense
from api.trip.models import Trip
from api.expense.serializers import ExpenseSerializer
from api.permissions import ObjectOwnerPermission


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, ObjectOwnerPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            trip_pk = self.kwargs.get("trip_pk")
            self.check_trip_user(trip_pk)
            return queryset.filter(trip_id=trip_pk)
        return queryset

    def check_trip_user(self, trip_pk: int) -> bool:
        """Checks whether the logged user is the owner of the trip."""

        try:
            trip = Trip.objects.get(pk=trip_pk)
        except ObjectDoesNotExist:
            raise exceptions.NotFound("Trip does not exists")
        if trip.user != self.request.user:
            raise exceptions.PermissionDenied()
