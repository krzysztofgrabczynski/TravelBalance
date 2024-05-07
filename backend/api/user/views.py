from rest_framework import views, status, generics, viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from api.user import serializers
from api.user.email import ActivationEmail


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    invalid_credentials_message = "Invalid credentials"
    user_inactive_message = "User is not active"

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        errors = {}
        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                if user.is_active:
                    token = self._create_user_auth_token(user)
                    return Response(
                        {"token": token.key},
                        status=status.HTTP_200_OK,
                    )

                else:
                    raise PermissionDenied
            raise ObjectDoesNotExist
        except PermissionDenied:
            errors.setdefault("errors", [])
            errors["errors"].append(
                {"inactive_user": self.user_inactive_message}
            )

        except ObjectDoesNotExist:
            errors.setdefault("errors", [])
            errors["errors"].append(
                {"invalid_credentials": self.invalid_credentials_message}
            )

        if errors:
            serializer._errors = errors
            raise exceptions.ValidationError(serializer.errors)

    def _create_user_auth_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token


class LogoutView(views.APIView):
    def post(self, request):
        self._delete_user_auth_token(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _delete_user_auth_token(self, request: HttpRequest) -> None:
        Token.objects.filter(user=request.user).delete()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        elif self.action == "account_activation":
            return serializers.AccountActivationSerializer
        elif self.action == "reset_password":
            return ...

        return self.serializer_class

    def perform_create(self, serializer):
        user = serializer.save()
        context = {"user": user}
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
    def reset_password(self, request):
        pass
