from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError



class CustomUserCreationForm(UserCreationForm):
        class Meta:
            model = CustomUser
            fields = ("username", "email")
            field_classes = {'username': UsernameField}


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        """
        allow login by active and verified users,
        and reject login by inactive and not verified users.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

        if not user.is_verified:
            raise ValidationError(
                self.error_messages['not verified'],
                code='inactive',
            )
