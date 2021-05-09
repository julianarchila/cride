""" Membership serializers. """

# Django REST Framework
from rest_framework import serializers

# Utilities
from django.utils import timezone

# Models
from cride.circles.models import Membership, Invitation

# Other serializers
from cride.users.serializers.users import UserModelSerializer

class MembershipModelSerializer(serializers.ModelSerializer):
    """ Membership model serializer. """
    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source="created", read_only=True)
    class Meta:
        """ Meta class. """
        model = Membership
        fields = (
            "user", "is_admin", "is_active",
            "used_invitations", "remaining_invitations",
            "invited_by", 
            "rides_taken", "rides_offered",
            "joined_at"
        )
        read_only_fields = (
            "user", 
            "used_invitations", 
            "invited_by", 
            "rides_taken", "rides_offered",
        )

class MembershipCreateSerializer(serializers.Serializer):
    invitation_code = serializers.CharField(min_length=8, max_length=50)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, value):
        """ Check is user is not already a member of the circle. """
        q = Membership.objects.filter(user=value, circle=self.context["circle"])
        if q.exists():
            raise serializers.ValidationError("User is already a circle member")
        return value


    def validate_invitation_code(self, value):
        try:
            invitation = Invitation.objects.get(
                code=value,
                circle=self.context["circle"],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid invitation code")

        self.context["invitation"] = invitation
        return value

    def validate(self, data):
        """ Verify circle is capable of accepting a new member. """
        circle = self.context["circle"]
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError("Circle has riched its members limit :(")

        return data

    def create(self, validated_data):
        circle = self.context["circle"]
        invitation = self.context["invitation"]
        user = validated_data["user"]

        # Create member
        member = Membership.objects.create(
            user=user,
            profile=user.profile,
            circle=circle,
            invited_by=invitation.issued_by,
            remaining_invitations=5
        )

        # Update invitation data
        invitation.used = True
        invitation.used_by = user
        invitation.used_at = timezone.now()
        invitation.save()


        # Update issuer data
        issuer = Membership.objects.get(
            user=invitation.issued_by,
            circle=circle
        )
        issuer.used_invitations += 1
        issuer.remaining_invitations -= 1
        issuer.save()

        return member 

    