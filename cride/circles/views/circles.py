""" Circle views. """

# Django REST framework.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Models
from cride.circles.models import Circle, Membership

# Serializers
from cride.circles.serializers import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """ Circle view set. """
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Circle.objects.all()
        if self.action == "list":
            return queryset.filter(is_public=True)
        return queryset

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

    
