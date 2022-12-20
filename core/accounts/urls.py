from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
]