from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('Login', CustomLoginView.as_view(), name='login'),
    path('Signup', SignupView.as_view(), name='signup'),
]