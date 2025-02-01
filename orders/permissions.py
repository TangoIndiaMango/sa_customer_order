from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Handle both Customer and Order models
        if hasattr(obj, "user"):
            return obj.user == request.user
        elif hasattr(obj, "customer"):
            return obj.customer.user == request.user
        return False
