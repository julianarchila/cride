""" Users api views. """

# Django

# Django Rest framework
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response


# Permisions
from rest_framework.permissions import (
    AllowAny, 
    IsAuthenticated
)
from cride.users.permissions import IsAccountOwner

# Models
from cride.users.models import User
from cride.circles.models import Circle

# Serializers
from cride.users.serializers.users import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
)
from cride.users.serializers.profiles import ProfileModelSerializer
from cride.circles.serializers.circles import CircleModelSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):
    """ User view set.
    Handle signup, login, account verification
    """
    queryset = User.objects.filter(is_active=True, is_client=True)
    serializer_class = UserModelSerializer
    lookup_field = "username"

    def get_permissions(self):
        """ Asign permissions based on action. """
        if self.action in ["signup", "login", "verify"]:
            permissions = [AllowAny]
        elif self.action in ["retrieve", "update", "partial_update"]:
            permissions = [IsAuthenticated,IsAccountOwner]
        else: 
            permissions = [IsAuthenticated]

        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """ User signup """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = {
            "status": "ok",
            "user": UserModelSerializer(user).data,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["POST"])
    def login(self, request):
        """Login action """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            "status": "ok",
            "user": UserModelSerializer(user).data,
            "token": token,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["POST"])
    def verify(self, request):
        """ Account verification """
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "message": "Congratulation, now go share some rides¡",
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True , methods=["PUT", "PATCH"])
    def profile(self, request, *args, **kwargs):
        user = self.get_object()
        profile = user.profile
        partial = request.method == "PATCH"
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data)
    

    def retrieve(self, request, *args, **kwargs):
        """ Add extra data to the response """
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        circles = Circle.objects.filter(
            members=request.user,
            membership__is_active=True
        )
        data = {
            "user": response.data,
            "circles": CircleModelSerializer(circles, many=True).data
        }
        response.data = data
        return response


    

