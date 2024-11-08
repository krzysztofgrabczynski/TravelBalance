from functools import wraps
from django.contrib.auth import get_user_model
from api.user.models import MyUser
from rest_framework.exceptions import PermissionDenied


User = get_user_model()


def check_if_subscriber(user: MyUser) -> bool:
    return user.groups.filter(name="subscriber").exists()


def add_trip_limit(func):
    max_trip_amount = 500

    @wraps(func)
    def wrapped(request, *args, **kwargs):
        user = request.user
        if not check_if_subscriber(user):
            if user.trips.count() >= max_trip_amount:
                raise PermissionDenied

        return func(request, *args, **kwargs)

    return wrapped
