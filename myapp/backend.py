from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from myapp.models import Userdata 
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from myapp.models import CustomToken 
from rest_framework.authentication import TokenAuthentication
# Replace with your custom user model

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Authenticate using email
            user = Userdata.objects.get(email=email)
            if user.check_password(password):  # Check if the password matches
                return user
        except Userdata.DoesNotExist:
            return None  # Return None if user doesn't exist
        return None

    def get_user(self, user_id):
        try:
            return Userdata.objects.get(pk=user_id)
        except Userdata.DoesNotExist:
            return None


"""

class CustomTokenAuthentication(TokenAuthentication):
    model = CustomToken

    def authenticate_credentials(self, key):
        print("CustomTokenAuthentication: Key received:", key)
        return super().authenticate_credentials(key)



class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            token_key = token.split('Token ')[1]
            token_obj = CustomToken.objects.get(key=token_key)
        except (IndexError, CustomToken.DoesNotExist):
            raise AuthenticationFailed('Invalid token')

        return (token_obj.user, token_obj)
"""

