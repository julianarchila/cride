""" Membership model. """

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel

class Membership(CRideModel):
    """ Memberhip model.
        a memberhips is table that holds the relation between
        an user and a circle.
    """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    circle = models.ForeignKey("circles.Circle", on_delete=models.CASCADE)

    is_admin = models.BooleanField(
        "circle admin",
        default=False,
        help_text="Circle admins can update circle's data and manage its members."
    )

    # Invitation
    used_invitations = models.PositiveSmallIntegerField(default=0)
    remaining_invitations = models.PositiveSmallIntegerField(default=0)
    invited_by = models.ForeignKey(
        "users.User", 
        null=True,
        on_delete=models.SET_NULL,
        related_name="invited_by"
    )

    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(
        "active status", 
        default=True, 
        help_text='only active useres can interact in the circl'
    )

    def __str__(self):
        """ Return username and circle. """
        return f"@{self.user.username} at {self.circle.slug_name}"

