from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum
from django.utils.decorators import method_decorator

from api.trip.models import Trip
from api.expense.models import Expense
from api.trip.serializers import TripSerializer, TripWithExpensesSerializer
from api.permissions import ObjectOwnerPermission
from api.subscription_restrictions import add_trip_limit


@method_decorator(add_trip_limit, name="create")
class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, ObjectOwnerPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list" or self.action == "get_trip_with_expenses":
            return queryset.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "get_trip_with_expenses":
            return TripWithExpensesSerializer
        return self.serializer_class

    @action(methods=["GET"], detail=False)
    def get_trip_with_expenses(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
