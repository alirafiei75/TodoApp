from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm

class CustomLoginView(LoginView):
    """class for custom login view"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        """custom dispatch
        to redirect authenticated user to home page"""       
        if request.user.is_authenticated:
            return redirect('todo:tasks')
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('todo:tasks')


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    """class for custom logout view"""
    template_name = 'accounts/logout.html'


class SignupView(CreateView):
    """class for custom signup view"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'