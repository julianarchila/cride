""" Users serializers. """

# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

 
# Django rest framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from cride.users.models import User, Profile

# Utilities
from datetime import timedelta
import jwt 


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
        user = User.objects.create_user(**data, is_verified=False)
        profile = Profile.objects.create(user=user)
        self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self, user):
        """Sending account verification email to given user."""
        token = self.gen_verification_token(user)
        subject = f"Welcome @{user.username}! Verify your account to start using the app."
        from_email = "Comparte Ride <noreply@comparteride.com>"

        content = render_to_string(
            "emails/users/account_verification.html", 
            {"token": token, "user": user}
        )

        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content , "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """ Generate a JWT that the user can use to verify its account. """
        exp_date = timezone.now() + timedelta(days=3)
        pay_load = {
            "user": user.username,
            "exp": int(exp_date.timestamp()),
            "type": "email_confirmation"
        }
        token = jwt.encode(pay_load, settings.SECRET_KEY, algorithm="HS256")
        return token


    

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
        if not user.is_verified:
            raise serializers.ValidationError("Account is not active yet :(")

        self.context["user"] = user
        return data

    def create(self, data):
        """Regenerate or retrive new token."""
        token, created = Token.objects.get_or_create(user=self.context["user"])

        return self.context["user"], token.key


