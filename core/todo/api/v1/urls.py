from django.urls import path
from .views import *

app_name = 'todo-api'

urlpatterns = [
    path('tasks', TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]