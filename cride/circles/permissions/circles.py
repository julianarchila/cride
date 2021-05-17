""" Circle custome permissions. """

# Django rest framework.
from rest_framework import permissions

# Models
from cride.circles.models import Membership


class IsCircleAdmin(permissions.BasePermission):
    """Allow access only to circle admins."""
    message = 'Only admins can edit circles.'

    def has_object_permission(self, request, view, obj):
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
