""" Rides custome permissions. """

# Django rest framework.
from rest_framework import permissions

# Models
from cride.circles.models import Membership

class IsRideOwner(permissions.BasePermission):
    """ Ensure ride is offered by requesting user. """
    message = "You are not the user who is offering the ride."
    def has_object_permission(self, request, view, obj):
        return obj.offered_by == request.user

class PassangerIsNotRideOwner(permissions.BasePermission):
    """ Ensure ride if offered by requesting user. """
    message = "Ride owner can't be a passenger."
    def has_object_permission(self, request, view, obj):
        return not obj.offered_by == request.user