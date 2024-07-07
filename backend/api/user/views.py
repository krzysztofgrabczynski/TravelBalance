from rest_framework import views, status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.contrib.auth.tokens import default_token_generator

from api.user import serializers
from api.user.email import ActivationEmail, ForgotPasswordEmail
from api.permissions import ObjectOwnerPermission


class LoginView(views.APIView):
    serializer_class = serializers.LoginSerializer

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


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    token_generator = default_token_generator
    permission_classes = [permissions.IsAuthenticated, ObjectOwnerPermission]

    SAFE_ACTIONS = [
        "create",
        "account_activation",
        "forgot_password",
        "forgot_password_check_token",
        "forgot_password_confirm",
    ]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        elif self.action == "account_activation":
            return serializers.AccountActivationSerializer
        elif self.action == "forgot_password":
            return serializers.ForgotPasswordSerializer
        elif self.action == "forgot_password_check_token":
            return serializers.EmailAndTokenSerializer
        elif self.action == "forgot_password_confirm":
            return serializers.ForgotPasswordConfirmSerializer
        elif self.action == "reset_password":
            return serializers.PasswordResetSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in self.SAFE_ACTIONS:
            return [permissions.AllowAny()]
        return super().get_permissions()

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
    def forgot_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.create_token()
        context = {"token": token.token, "to": token.user.email}
        ForgotPasswordEmail(self.request, context).send()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def forgot_password_check_token(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["post"], detail=False)
    def forgot_password_confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.set_password(serializer.validated_data["password"])
        serializer.user.save()
        serializer.delete_user_tokens(serializer.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=["POST"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.user.set_password(serializer.validated_data["password"])
        serializer.user.save()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
