from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum
from django.utils.decorators import method_decorator

from api.trip.models import Trip
from api.expense.models import Expense
from api.trip.serializers import TripReadSerializer, TripWriteSerializer
from api.permissions import ObjectOwnerPermission
from api.subscription_restrictions import add_trip_limit


@method_decorator(add_trip_limit, name="create")
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripReadSerializer
    permission_classes = [IsAuthenticated, ObjectOwnerPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            return queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self, *args, **kwargs):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
            or self.action == "destroy"
        ):
            return TripWriteSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        user_trips = Trip.objects.filter(user=request.user)
        total_trips_amount = user_trips.count()
        visited_countries_amount = sum(
            [t.countries.count() for t in user_trips]
        )
        spendings = sum([c.trip_cost for c in user_trips])
        extra_content = {
            "total_trips_amount": total_trips_amount,
            "visited_countries_amount": visited_countries_amount,
            "spendings": spendings,
        }

        return Response({"statistics": extra_content, "trips": response.data})

    @action(methods=["GET"], detail=True)
    def get_cost_per_category(self, request, *args, **kwargs):
        trip = self.get_object()
        trip_expenses = trip.expenses
        aggregate_per_category = trip_expenses.values("category").annotate(
            cost=Sum("cost")
        )
        data = {key: 0 for key in Expense.ExpenseCategory.values}
        for c in aggregate_per_category:
            data[c["category"]] = c["cost"]

        return Response(data)
