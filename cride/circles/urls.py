"""Circles URLs module."""

# Django
from django.urls import path, include

# Views
from cride.circles.views import list_circles


urlpatterns = [
    path("circles/", list_circles),
] 
