""" Users serializers. """

# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
 
# Django rest framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from cride.users.models import User, Profile


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

class UserSignUpSerializer(serializers.Serializer):
    """User signup serializers. 
    Handle signup data validation and user/profile creation.
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be in the format : +999999999 up to 15 digits"
    )
    phone_number = serializers.CharField(validators=[phone_regex],max_length=17)


    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):

        # Verify passwords match. 
        passwd = data["password"]
        passwd_conf = data["password_confirmation"]
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords do not match.")
        password_validation.validate_password(passwd)

        return data

    def create(self,data):
        data.pop("password_confirmation")
        user = User.objects.create_user(**data)
        profile = Profile.objects.create(user=user)
        return user

    

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


