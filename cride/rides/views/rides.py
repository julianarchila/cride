""" Ride views. """

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404

# Serializers
from cride.rides.serializers import (
    CreateRideSerializer,
    RideModelSerializer
)

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions.memberships import IsActiveCircleMember

# Models
from cride.circles.models import Circle

# Utilities
from datetime import timedelta
from django.utils import timezone



class RideViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated, IsActiveCircleMember]

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ["departure_location", "arrival_location"]
    ordering_fields = ["departure_date", "arrival_date", "available_seats"]
    ordering = ["departure_date", "arrival_date", "-available_seats"]
    # filter_fields = ["", "is_limited"]

    def dispatch(self, request, *args, **kwargs):
        """ Verify that the circle exists. """
        slug_name = kwargs["slug_name"]
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(RideViewSet, self).get_serializer_context()
        context["circle"] = self.circle
        return context

    def get_serializer_class(self):
        """ Provide a different serializer dependign on the action. """
        if self.action == "create":
            return CreateRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        offset = timezone.now() + timedelta(minutes=5)
        return self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1
        )
