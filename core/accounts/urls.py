from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('logged_out', CustomLogoutView.as_view(), name='logout'),
    path('api/v1/', include('accounts.api.v1.urls')),
]