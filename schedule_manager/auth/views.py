from rest_framework import status
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.generics import GenericAPIView
from schedule_manager.auth.serializers import (
    RegisterUserSerializer,
    CustomTokenObtainPairSerializer,
    CustomCookieTokenRefreshSerializer
)
from schedule_manager.utils.jwt_auth import (
    set_cookies,
    logout_and_revoke_tokens,
    refresh_and_set_jwt_cookies
)
from rest_framework_simplejwt.tokens import TokenError
from dj_rest_auth.jwt_auth import CookieTokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView


class RegisterView(GenericAPIView):
    """An endpoint for user registration."""

    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        """Handle registration request."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Successfully Registered"},
            status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):
    """An endpoint for user to login."""

    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """Handle login request."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_http_cookie_only = self.request.data.get("is_http_cookie_only", False)

        # Set both token in the cookie
        return set_cookies(
            response=Response(serializer.validated_data),
            access_token=serializer.validated_data["access"],
            refresh_token=serializer.validated_data["refresh"],
            is_http_cookie_only=is_http_cookie_only
        )


class LogoutView(GenericAPIView):
    """An endpoint for user to logout."""

    permission_classes = [IsAuthenticated]
    serializer_class = CustomCookieTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        """Handle logout request."""

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data.get("refresh")
            is_http_cookie_only = request.data.get("is_http_cookie_only", False)

            # Update the last logout time
            request.user.update_last_logout_at()

            # Blacklist the refresh token
            response = logout_and_revoke_tokens(
                response=Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK),
                refresh_token=refresh_token,
                is_http_cookie_only=is_http_cookie_only
            )

            return response

        except TokenError as error:
            return Response(
                {"detail": f"{error}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class TokenRefreshView(BaseTokenRefreshView):
    """An endpoint for user to refresh token."""

    # This will handle for getting a new refresh and access token
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        """Set the access token in the cookie."""
        is_http_cookie_only = request.data.get("is_http_cookie_only", False)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            # Set the access token in the cookie
            try:
                response = refresh_and_set_jwt_cookies(
                    response=response,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    is_http_cookie_only=is_http_cookie_only
                )

            except Exception as error:
                response = Response(
                    {"detail": f"{error}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().finalize_response(request, response, *args, **kwargs)
