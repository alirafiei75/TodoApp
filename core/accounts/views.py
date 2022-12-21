from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):       
        if request.user.is_authenticated:
            username = self.request.user.username 
            return redirect('todo:tasks', username=username)
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        username = self.request.POST.get('username')
        if username is not None:
            return reverse_lazy('todo:tasks', kwargs={'username': username})


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'accounts/logout.html'


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'