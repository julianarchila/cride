"""Users URLs module."""

# Django
from django.urls import path, include

# Views
from .views.users import (
    UserLoginAPIView, 
    UserSignUpAPIView, 
    AccountVerificationAPIView, 
)



urlpatterns = [
    path("users/login/", UserLoginAPIView.as_view(), name="login"),
    path("users/signup/", UserSignUpAPIView.as_view(), name="signup"),
    path("users/verify/", AccountVerificationAPIView.as_view(), name="verify"),
] 
