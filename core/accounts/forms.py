from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = CustomUser
            fields = ("username", "email")
            field_classes = {'username': UsernameField}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")