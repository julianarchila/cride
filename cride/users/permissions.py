""" User custome permissions. """

# Django rest framework.
from rest_framework import permissions

# Models


class IsAccountOwner(permissions.BasePermission):
    """Allow user retrive only to account owner."""
    message = 'You are not allow to see this information.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user
