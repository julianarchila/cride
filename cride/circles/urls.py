"""Circles URLs module."""

# Django
from django.urls import path, include

# Views
from cride.circles.views import (
    list_circles,
    create_circle
)


urlpatterns = [
    path("circles/", list_circles),
    path("circles/create/", create_circle),
] 
