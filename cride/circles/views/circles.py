""" Circle views. """

# Django REST framework.
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Custome permissions
from cride.circles.permissions.circles import IsCircleAdmin

# Models
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers import CircleModelSerializer

class CircleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    """ Circle view set. """
    serializer_class = CircleModelSerializer
    lookup_field = "slug_name"

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ["name", "slug_name", "about"]
    ordering_fields = ["name", "rides_taken", "rides_offered"]
    ordering = ["-members__count", "-rides_offered", "-rides_taken"]
    filter_fields = ["verified", "is_limited"]



    def get_queryset(self):
        queryset = Circle.objects.all()
        if self.action == "list":
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """ Define permisions for the viewset """
        # permission_classes = []
        permission_classes = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permission_classes.append(IsCircleAdmin)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True, 
            remaining_invitations=10
        )

    
