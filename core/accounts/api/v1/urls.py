from django.urls import path, include
from .views import *

app_name = 'accounts-api'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('token/login/', CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', TokenLogout.as_view(), name='token-logout'),
]