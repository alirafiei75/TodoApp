from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import CustomUser
from rest_framework.authtoken.serializers import AuthTokenSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration"""

    password1 = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "password1"]

    def validate(self, attrs):
        """validation of given attributes"""
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "passwords does not match"})
        if not attrs.get("email"):
            raise serializers.ValidationError(
                {"detail": "please enter an email address"}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return super().create(validated_data)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    """Customizing AuthTokenSerializer for token authentication."""

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError({"detail": "user is not verified."})
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizing TokenObtainPairSerializer for jwt authentication."""

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["username"] = self.user.username
        validated_data["user_id"] = self.user.id
        if not self.user.is_verified:
            raise serializers.ValidationError({"detail": "user is not verified."})
        return validated_data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """validation of given attributes"""
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "passwords does not match"})

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return super().validate(attrs)


class VerificationResendSerializer(serializers.Serializer):
    """serializer for resending verification email."""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"detail": "user does not exist"})
        if user_obj.is_verified:
            raise serializers.ValidationError({"detail": "user is already verified"})
        attrs["user"] = user_obj
        return super().validate(attrs)


class RequestResetPasswordSerializer(serializers.Serializer):
    """serializers for requesting password reset."""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"detail": "user does not exist"})
        attrs["user"] = user_obj
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """serializer for resetting password."""

    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """validation of given attributes"""
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "passwords does not match"})

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return super().validate(attrs)
