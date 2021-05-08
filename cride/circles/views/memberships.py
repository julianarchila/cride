""" Circle memebershp views """

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Models
from cride.circles.models import Circle
from cride.circles.models import Membership 

# Serializers
from cride.circles.serializers.memberships import MembershipModelSerializer

class MembershipViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    """ Circle membership viewset """ 

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """ Verify that the circle exists. """
        slug_name = kwargs["slug_name"]
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        ) 
