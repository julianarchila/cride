""" Ride views. """

# Django REST Framework
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action

# Serializers
from cride.rides.serializers import (
    CreateRideSerializer,
    RideModelSerializer,
    JoinRideSerializer
)

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from cride.circles.permissions.memberships import IsActiveCircleMember
from cride.rides.permissions.rides import IsRideOwner,PassangerIsNotRideOwner 

# Models
from cride.circles.models import Circle

# Utilities
from datetime import timedelta
from django.utils import timezone



class RideViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):


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

    def get_permissions(self):
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ["update", "partial_update"]:
            permissions.append(IsRideOwner)

        if self.action == "join":
            permissions.append(PassangerIsNotRideOwner)

        return [p() for p in permissions]


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
    @action(detail=True, methods=["POST"])
    def join(self, request, *args, **kwargs):
        """ Add requesting user to ride. """
        ride = self.get_object()
        serializer = JoinRideSerializer(
            ride,
            data={"passenger": request.user.id},
            context={"ride": ride, "circle": self.circle},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)
