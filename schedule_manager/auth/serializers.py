from typing import Any, Dict
from django.db import transaction
from rest_framework import serializers
from schedule_manager.models import User
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from schedule_manager.serializers import UserSerializer
from dj_rest_auth.jwt_auth import CookieTokenRefreshSerializer
from schedule_manager.utils.validator import password_validator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterUserSerializer(UserSerializer):
    """
    Registration serializer.
    """

    password = serializers.CharField(
        min_length=8,
        required=True,
        write_only=True,
        max_length=255,
        style={"input_type": "password"},
        error_messages={
            "blank": "This field is required",
            "null": "This field is required.",
        }
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
        ]
        extra_fields = {
            "id": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_active": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

    def validate_password(self, value: str) -> str:
        """
        Validate password.
        """
        password_validator(value)
        return value

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Override the create method.
        """

        password = validated_data.pop("password")
        with transaction.atomic():
            # Check a user type for doctor
            User.objects.create_user(password=password, **validated_data)
            return validated_data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom login serializer."""

    is_http_cookie_only = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the credentials."""

        if "email" in attrs:
            attrs["email"] = attrs["email"].lower()

        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data

        # Update last timestamp of the user
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class CustomCookieTokenRefreshSerializer(CookieTokenRefreshSerializer):
    """Custom refresh token serializer."""
    is_http_cookie_only = serializers.BooleanField(required=False)
