from rest_framework import views, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth.tokens import default_token_generator

from api.user import serializers
from api.user.email import ActivationEmail, ForgotPasswordEmail


class LoginView(views.APIView):
    serializer_class = serializers.LoginSerializer
    default_error_messages = {
        "invalid_credentials": "Invalid credentials",
        "user_inactive": "User is not active",
    }

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"token": serializer.token.key},
            status=status.HTTP_200_OK,
        )


class LogoutView(views.APIView):
    def post(self, request):
        self._delete_user_auth_token(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _delete_user_auth_token(self, request: HttpRequest) -> None:
        Token.objects.filter(user=request.user).delete()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    token_generator = default_token_generator

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        elif self.action == "account_activation":
            return serializers.AccountActivationSerializer
        elif self.action == "forgot_password":
            return serializers.ForgotPasswordSerializer
        elif self.action == "forgot_password_confirm":
            return serializers.ForgotPasswordConfirmSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        user = serializer.save()
        context = {
            "user": user,
            "token_generator": self.token_generator,
            "to": user.email,
        }
        ActivationEmail(self.request, context).send()
        return user

    @action(
        methods=["get"],
        detail=False,
        url_path=r"account-activation/(?P<uidb64>\w+)/(?P<token>[-\w]+)",
        url_name="account_activation",
    )
    def account_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.create_token()
        context = {"token": token.token, "to": token.user.email}
        ForgotPasswordEmail(self.request, context).send()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def forgot_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.set_password(serializer.validated_data["password"])
        serializer.user.save()
        serializer.delete_user_tokens(serializer.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
