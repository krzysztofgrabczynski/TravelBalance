from rest_framework import permissions, exceptions
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from api.trip.models import Trip


User = get_user_model()


class ObjectOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        SAFE_METHODS = ["POST"]

        if request.method in SAFE_METHODS:
            return True

        if hasattr(obj, "user"):
            if request.user == obj.user:
                return True

        if isinstance(obj, User):
            if request.user == obj:
                return True

        return False


class TripOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        kwargs = request.parser_context["kwargs"]
        assert (
            view.trip_lookup_field in kwargs
        ), f"Missing {view.trip_lookup_field} in request arguments."

        trip_pk = kwargs[view.trip_lookup_field]
        self.check_trip_user(request, trip_pk)

        return True

    @staticmethod
    def check_trip_user(request: Request, trip_pk: int) -> None:
        """Checks whether the logged user is the owner of the trip."""

        try:
            trip = Trip.objects.get(pk=trip_pk)
        except ObjectDoesNotExist:
            raise exceptions.NotFound("Trip does not exists")
        if trip.user != request.user:
            raise exceptions.PermissionDenied()
