""" Users api views. """

# Django

# Django Rest framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# Serializers
from cride.users.serializers.users import (
    UserLoginSerializer,
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
)

class UserLoginAPIView(APIView):
    """ User login api view. """

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()

        data = {
            "status": "ok",
            "user": UserModelSerializer(user).data,
            "token": token,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
        

class UserSignUpAPIView(APIView):
    """ User login api view. """

    def post(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = {
            "status": "ok",
            "user": UserModelSerializer(user).data,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
        
class AccountVerificationAPIView(APIView):
    """ Account verification api view. """

    def post(self, request, *args, **kwargs):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "message": "Congratulation, now go share some rides¡",
        }
        return Response(data=data, status=status.HTTP_200_OK)