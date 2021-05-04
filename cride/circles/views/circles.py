""" Circle views. """

# Django REST framework.
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = (IsAuthenticated,)
    lookup_field = "slug_name"

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

    
