""" Users serializers. """

# Django
from django.contrib.auth import authenticate
 
# Django rest framework
from rest_framework import serializers


class UserLoginSerializer(serializers.Serializer):
    """User login serializers. 
    Handle the login request data.
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self,data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            return serializers.ValidationError("Invalid credentials.")
        return data