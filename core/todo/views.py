from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Task
from .forms import CreateTaskForm

class TasksView(LoginRequiredMixin, ListView, FormView):
    model = Task
    template_name = 'todo/tasks.html'
    context_object_name = 'tasks'
    form_class = CreateTaskForm
    success_url = reverse_lazy('accounts:login')
    object_list = 'tasks'

    def get_queryset(self, *args, **kwargs):
        qs = super(TasksView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(user__username=self.kwargs['username'])
        return qs

    def get_context_data(self, **kwargs):
        username = self.request.user.username 
        context = super().get_context_data(**kwargs)
        context['user'] = Task.objects.filter(user__username=username)[0]
        return context

    def post(self, request, *args, **kwargs):
        return FormView.post(self, request, *args, **kwargs)


