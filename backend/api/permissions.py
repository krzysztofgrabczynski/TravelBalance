from rest_framework import permissions
from django.contrib.auth.models import User


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
