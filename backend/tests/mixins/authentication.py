from rest_framework.authtoken.models import Token
from django.test.client import Client
from django.contrib.auth.models import AbstractUser


class AuthenticateUserWithTokenMixin:
    def authenticate_user(self, client: Client, user: AbstractUser) -> None:
        auth_token, _ = Token.objects.get_or_create(user=user)
        token = "Token " + str(auth_token)
        client.login(username="test_user", password="test123")
        client.credentials(HTTP_AUTHORIZATION=token)
