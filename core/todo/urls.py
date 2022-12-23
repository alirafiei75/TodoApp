from django.urls import path
from .views import *

app_name = 'todo'

urlpatterns = [
    path('tasks', TasksView.as_view(), name='tasks'),
    path('create-task/', TaskCreateView.as_view(), name='create'),
    path('edit-task/<int:pk>', TaskEditView.as_view(), name='edit'),
    path('delete-task/<int:pk>', TaskDeleteView.as_view(), name='delete')
]