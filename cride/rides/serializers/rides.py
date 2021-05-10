""" Rides serializers. """

# Django REST Framework
from rest_framework import serializers

# Models
from cride.users.models import User
from cride.rides.models import Ride
from cride.circles.models import Membership

# Serializers
from cride.users.serializers.users import UserModelSerializer

# Utilities
from datetime import timedelta
from django.utils import timezone


class RideModelSerializer(serializers.ModelSerializer):
    """ Ride model serializer."""
    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()

    passengers = UserModelSerializer(read_only=True, many=True)
    class Meta:
        """ Meta class. """
        model = Ride
        fields = "__all__"
        read_only_fields = (
            "offered_by",
            "offered_in",
            "rating"
        )

    def update(self, instance, validated_data):
        if timezone.now() >= instance.departure_date:
            raise serializers.ValidationError("On going rides can not be modified.")

        return super(RideModelSerializer, self).update(instance, validated_data)

class CreateRideSerializer(serializers.ModelSerializer):

    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)
    
    class Meta:
        """ Meta class. """
        model = Ride
        exclude = ("offered_in", "passengers", "rating", "is_active")

    def validate_departure_date(self, value):
        """ Validate a rides is not staring in the past. """
        min_date = timezone.now() + timedelta(minutes=10)
        if value < min_date:
            raise serializers.ValidationError("Departure time must be at least pass a 15 minute window.")
        return value

    def validate(self, data):
        """Validate.
        Verify that the person who offeres the ride is a member of the circle
        and also the person who is making the request.
        """
        if self.context["request"].user != data["offered_by"]:
            raise serializers.ValidationError("Rides offered on behalf of others are not allow")

        user = data["offered_by"]
        circle = self.context["circle"]
        try:
            membership = Membership.objects.get(user=user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError("User is not a active member of the circle.")

        if data["arrival_date"] <= data["departure_date"]:
            raise serializers.ValidationError("Arrival date must not be before departure date.")

        self.context["membership"] = membership
        return data


    def create(self, validated_data):
        """Create ride and update circle,profile and membership stats. """
        circle = self.context["circle"]
        ride = Ride.objects.create(**validated_data, offered_in=circle)

        # Circle
        circle.rides_offered += 1
        circle.save()

        # Membership
        membership = self.context["membership"]
        membership.rides_offered += 1
        membership.save()

        # Profile
        profile = validated_data["offered_by"].profile
        profile.rides_offered += 1
        profile.save()

        return ride

        

class JoinRideSerializer(serializers.ModelSerializer):
    """ Join ride serializer. """
    passenger = serializers.IntegerField()
    class Meta:
        model = Ride
        fields = ("passenger",)

    def validate_passenger(self, data):
        """ Check passanger exists and is a circle member. """
        try:
            user = User.objects.get(pk=data)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid passanger")

        circle = self.context["circle"]

        try:
            membership = Membership.objects.get(user=user, circle=circle, is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError("User is not a active member of the circle.")


        self.context["member"] = membership 
        self.context["user"] = user
        return data

    def validate(self, data):
        """Verify ride allows new passangers."""
        ride = self.context["ride"]

        # Check time
        if ride.departure_date <= timezone.now():
            raise serializers.ValidationError("Ride already started :(")

        # Check available seats
        if ride.available_seats < 1:
            raise serializers.ValidationError("Ride is alreay full :(")

        # Check user is not already in the ride.
        if ride.passengers.filter(pk=data["passenger"]).exists():
            raise serializers.ValidationError("Passanger is already in this trip.")

        return data

    def update(self, instance, data):
        """ Add requesting user to the passangers list of the ride
        and update the stats."""
        ride = self.context["ride"]
        circle = self.context["circle"]
        user = self.context["user"]

        ride.passengers.add(user)
        ride.available_seats -= 1
        ride.save()

        # Profile stats 
        profile = user.profile
        profile.rides_taken += 1
        profile.save()

        # Membership
        member = self.context["member"]
        member.rides_taken += 1
        member.save()

        # Circle
        circle.rides_taken += 1
        circle.save()

        return ride