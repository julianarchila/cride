"""Rides URLs module."""

# Django
from django.urls import path, include

# Django REST framework.
from rest_framework.routers import DefaultRouter

# Views
from .views import rides as ride_views 

router = DefaultRouter()

router.register(
    r"circles/(?P<slug_name>[a-zA-Z0-9_-]+)/rides",
    ride_views.RideViewSet,
    basename="ride"
)

urlpatterns = [
    path("", include(router.urls))
]