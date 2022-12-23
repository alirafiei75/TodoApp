from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task

class TasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self, *args, **kwargs):
        qs = super(TasksView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(user__username=self.kwargs['username'])
        return qs


class TaskCreateView(CreateView):
    template_name = 'todo/create.html'
    model = Task
    fields = ['user', 'title']



