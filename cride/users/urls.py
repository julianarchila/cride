"""Users URLs module."""

# Django
from django.urls import path, include

# Views
from .views import UserLoginAPIView



urlpatterns = [
    path("users/login", UserLoginAPIView.as_view())
] 
