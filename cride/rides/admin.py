""" Rides admin. """

# Django
from django.contrib import admin

# Models
from cride.rides.models import Ride

admin.site.register(Ride)
