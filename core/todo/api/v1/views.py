from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskSerializer, TasksSerializer
from .permissions import IsOwner
from ...models import Task

class TaskListView(ListCreateAPIView):
    """Generic view for showing the list of tasks"""
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.filter(user=user)
        return qs
        

class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """Generic view for showing the details of a task"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
