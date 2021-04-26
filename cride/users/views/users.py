""" Users api views. """

# Django

# Django Rest framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# Serializers
from cride.users.serializers import UserLoginSerializer

class UserLoginAPIView(APIView):
    """ User login api view. """

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        data = {
            "status": "ok",
            "token": token,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
        