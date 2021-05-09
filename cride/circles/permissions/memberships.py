""" Memberhips custome permissions. """

# Django rest framework.
from rest_framework import permissions

# Models
from cride.circles.models import Membership

class IsActiveCircleMember(permissions.BasePermission):
    """Allow access only to circle active members.

    Exptect that the views implementing this permision
    have a 'circle' attribute assigned.
    """

    def has_permission(self, request, view):
        """Verify user is an active member of the circle. """
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False

        return True

class IsSelfMember(permissions.BasePermission):
    """Only allow user to access its own information"""

    def has_permission(self, request, view):
        return view.get_object().user == request.user