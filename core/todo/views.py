from django.views.generic import ListView
from .models import Task

class TasksView(ListView):
    model = Task
    template_name = 'todo/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self, *args, **kwargs):
        qs = super(TasksView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(user__username=self.kwargs['username'])
        return qs
