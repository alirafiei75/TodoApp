from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer, TasksSerializer
from .permissions import IsOwner, IsVerifiedUser
from .paginations import DefaultPagination
from ...models import Task
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class TaskListView(ListCreateAPIView):
    """Generic view for showing the list of tasks"""

    serializer_class = TasksSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["completed"]
    search_fields = ["title"]
    ordering_fields = ["created_date"]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.filter(user=user)
        return qs


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """Generic view for showing the details of a task"""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
