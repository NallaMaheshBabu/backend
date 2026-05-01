# myapp/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import CustomToken

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # No token provided, treat as guest

        if not auth_header.startswith("Token "):
            raise exceptions.AuthenticationFailed('Authorization header must start with Token')

        token_key = auth_header[6:]  # strip "Token "

        try:
            token = CustomToken.objects.get(key=token_key)
        except CustomToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        return (token.user, token)