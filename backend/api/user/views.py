from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpRequest

from api.user.serializers import LoginSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    error_message = "Invalid credentials"

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if user:
            token = self._create_user_auth_token(user)
            return Response({"token": token.key, "status": status.HTTP_200_OK})

        return Response(
            {
                "error": self.error_message,
                "status": status.HTTP_401_UNAUTHORIZED,
            }
        )

    def _create_user_auth_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token


class LogoutView(views.APIView):
    def post(self, request):
        self._delete_user_auth_token(request)
        return Response({"status": status.HTTP_200_OK})

    def _delete_user_auth_token(self, request: HttpRequest) -> None:
        Token.objects.filter(user=request.user).delete()
