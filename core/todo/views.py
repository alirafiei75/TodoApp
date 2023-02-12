from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task


class TasksView(LoginRequiredMixin, ListView):
    """class for tasks list view"""

    model = Task
    template_name = "todo/tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        """getting tasks from the database
        based on current user"""
        current_user = self.request.user
        tasks = self.model.objects.filter(user=current_user)
        tasks = tasks.order_by("-created_date")
        return tasks

    def get_context_data(self, **kwargs):
        """passing extra data (user) to context"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    """class view for creating a new task"""

    template_name = "todo/create.html"
    model = Task
    fields = ["user", "title"]
    success_url = reverse_lazy("todo:tasks")

    def get_context_data(self, **kwargs):
        """passing extra data (user) to context
        to fill user field of the form automatically"""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        return context


class TaskCompleteView(LoginRequiredMixin, UpdateView):
    """class view to edit a task
    and set it to completed state"""

    template_name = "todo/complete.html"
    model = Task
    fields = [
        "completed",
    ]
    success_url = reverse_lazy("todo:tasks")


class TaskEditView(LoginRequiredMixin, UpdateView):
    """class view to edit a task's title"""

    template_name = "todo/edit.html"
    model = Task
    fields = [
        "title",
    ]
    success_url = reverse_lazy("todo:tasks")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    """class view to delete a task"""

    template_name = "todo/delete.html"
    model = Task
    success_url = reverse_lazy("todo:tasks")
