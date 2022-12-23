from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('<str:username>', TasksView.as_view(), name='tasks'),
    path('<str:username>/create/', TaskCreateView.as_view(), name='create')
]