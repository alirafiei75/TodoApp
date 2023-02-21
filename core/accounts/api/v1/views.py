from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from ...models import CustomUser
from .serializers import *
from ..utils import EmailThread


class RegistrationAPIView(generics.GenericAPIView):
    """API view for registration."""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(CustomUser, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/verification.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()

            return Response(
                {
                    "detail": "account created successfully. please visit your email inbox to activate your account."
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class VerificationAPIView(APIView):
    """API view for verification of a user after registration."""

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "token is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = CustomUser.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response(
                {"detail": "your account has already been verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"detail": "your account is now verified."},
            status=status.HTTP_200_OK,
        )


class VerificationResendAPIView(generics.GenericAPIView):
    """API view for resending verification email."""

    serializer_class = VerificationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerificationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/verification.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "activation link resent successfully."},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class RequestResetPasswordAPIView(generics.GenericAPIView):
    """API view for when user forgots password"""

    serializer_class = RequestResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = RequestResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/reset_password.tpl",
            {"user_id": user_obj.id, "token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"detail": "please check your email inbox to reset your password."},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordAPIView(generics.GenericAPIView):
    """API view for resetting password"""

    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "token is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = CustomUser.objects.get(pk=user_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user_obj.set_password(serializer.data.get("new_password"))
            user_obj.save()

            return Response(
                {"detail": "password changed successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    """Customizing API view for token authentication."""

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.id, "username": user.username}
        )


class TokenLogout(APIView):
    """class for discarding generated token or logging out."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {"detail": "token discarded successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """customizing creating jwt view"""

    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordAPIView(generics.GenericAPIView):
    """View class for changing the password."""

    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "Wrong password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response(
                {"detail": "password changed successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
