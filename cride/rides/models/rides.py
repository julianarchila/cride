""" Ride model. """

# Djnago
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Ride(CRideModel):
    offered_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    offered_in = models.ForeignKey("circles.Circle", on_delete=models.SET_NULL, null=True)
    passengers = models.ManyToManyField("users.User", related_name="passengers")

    available_seats = models.PositiveSmallIntegerField(default=1)
    comments = models.TextField(blank=True, null=True)

    departure_location = models.CharField(max_length=250)
    departure_date = models.DateTimeField()

    arrival_location = models.CharField(max_length=250)
    arrival_date = models.DateTimeField()

    rating = models.FloatField(null=True)

    is_active = models.BooleanField(
        "active status",
        default=True,
        help_text="Used for disabling the ride or finish it."
    )

    def __str__(self):
        """ Ride details. """
        return f"{self.departure_location} to {self.arrival_location} | {self.departure_date} - {self.arrival_date} "
