from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('Login')
    template_name = 'accounts/signup.html'