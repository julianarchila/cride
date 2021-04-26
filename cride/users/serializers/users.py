""" Users serializers. """

# Django
from django.contrib.auth import authenticate
 
# Django rest framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

# Models
from cride.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email', 
            'phone_number'
        )

class UserLoginSerializer(serializers.Serializer):
    """User login serializers. 
    Handle the login request data.
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self,data):
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        self.context["user"] = user
        return data

    def create(self, data):
        """Regenerate or retrive new token."""
        token, created = Token.objects.get_or_create(user=self.context["user"])

        return self.context["user"], token.key