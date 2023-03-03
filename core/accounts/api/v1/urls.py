from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import *

app_name = "accounts-api"

urlpatterns = [
    # Registration
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    # User Verification
    path(
        "verification/confirm/<str:token>",
        VerificationAPIView.as_view(),
        name="verification",
    ),
    path(
        "verification/resend/",
        VerificationResendAPIView.as_view(),
        name="verification-resend",
    ),
    # Change Password
    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    # Forget/Reset Password
    path(
        "request-reset-password/",
        RequestResetPasswordAPIView.as_view(),
        name="request-reset-password",
    ),
    path(
        "reset-password/uid/<int:user_id>/<str:token>",
        ResetPasswordAPIView.as_view(),
        name="reset-password",
    ),
    # Token Authentication
    path("token/login/", CustomObtainAuthToken.as_view(), name="token-login"),
    path("token/logout/", TokenLogout.as_view(), name="token-logout"),
    # JWT Authentication
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    path("weather", WeatherView.as_view(), name="weather"),
]
