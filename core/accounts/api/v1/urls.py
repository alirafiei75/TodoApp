from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import *

app_name = 'accounts-api'

urlpatterns = [
    # Registration
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    # Change Password
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    # Token Authentication
    path('token/login/', CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', TokenLogout.as_view(), name='token-logout'),
    # JWT Authentication
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]