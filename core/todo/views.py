from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task


class TasksView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    template_name = 'todo/create.html'
    model = Task
    fields = ['user', 'title']
    success_url = reverse_lazy('todo:tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context


class TaskCompleteView(LoginRequiredMixin, UpdateView):
    template_name = 'todo/complete.html'
    model = Task
    fields = ['completed',]
    success_url = reverse_lazy('todo:tasks')


class TaskEditView(LoginRequiredMixin, UpdateView):
    template_name = 'todo/edit.html'
    model = Task
    fields = ['user', 'title']
    success_url = reverse_lazy('todo:tasks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'todo/delete.html'
    model = Task
    success_url = reverse_lazy('todo:tasks')