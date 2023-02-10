from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for registration"""
    password1 = serializers.CharField(max_length=150, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password1']

    def validate(self, attrs):
        """validation of given attributes"""
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail': 'passwords does not match'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password1', None)
        return super().create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizing TokenObtainPairSerializer for jwt authentication."""
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['username'] = self.user.username
        validated_data['user_id'] = self.user.id
        return validated_data