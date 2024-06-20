from rest_framework import permissions


class ObjectOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        SAFE_METHODS = ["POST"]

        if request.method in SAFE_METHODS:
            return True
        if request.user == obj.user:
            return True
        return False
