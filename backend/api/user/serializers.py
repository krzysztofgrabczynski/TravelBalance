from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import (
    ObjectDoesNotExist,
    ImproperlyConfigured,
    PermissionDenied,
)

from api.user.models import ForgotPasswordToken

# class CustomErrorResponseMixin:
#     def is_valid(self, *args, **kwargs):
#         errors = {}
#         try:
#             return super().is_valid(*args, **kwargs)
#         except serializers.ValidationError as exc:
#             errors.setdefault(
#                 "errors",
#                 [{key: value[0]} for key, value in exc.detail.items()],
#             )
#             self._errors = errors
#             raise serializers.ValidationError(self.errors)

#     def to_internal_value(self, data):
#         errors = OrderedDict()
#         try:
#             return super().to_internal_value(data)
#         except (serializers.ValidationError, ValidationError) as exc:
#             errors.setdefault("errors", [])
#             for error in exc.detail.values():
#                 if not isinstance(error, dict):
#                     error = {
#                         "error": error[0],
#                         "status": status.HTTP_400_BAD_REQUEST,
#                     }
#                 errors["errors"].append(error)
#             raise serializers.ValidationError(errors)


class UserCreateMixin:
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, style={"input_type": "password"}
    )

    default_error_messages = {
        "invalid_credentials": "Invalid credentials",
        "user_inactive": "User is not active",
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        username = validated_data["username"]
        password = validated_data["password"]

        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                if user.is_active:
                    self.token = self._create_user_auth_token(user)
                    return validated_data

                else:
                    raise PermissionDenied
            raise ObjectDoesNotExist

        except PermissionDenied:
            key_error = "user_inactive"
            raise serializers.ValidationError(
                {"user_inactive": self.error_messages[key_error]},
                code=key_error,
            )
        except ObjectDoesNotExist:
            key_error = "invalid_credentials"
            raise serializers.ValidationError(
                {"invalid": self.error_messages[key_error]},
                code=key_error,
            )

    def _create_user_auth_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password2 = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    default_error_messages = {
        "unique_email": "User with that email already exists",
        "invalid_re_password": "Password fields must be the same",
    }

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            "password": {
                "required": True,
                "write_only": True,
                "validators": [validate_password],
            },
        }

    def validate_email(self, email: str) -> str:
        if User.objects.filter(email=email).exists():
            key_error = "unique_email"
            raise serializers.ValidationError(
                {"email": self.error_messages[key_error]}, code=key_error
            )

        return email

    def validate(self, attrs: dict) -> dict:
        if not attrs["password"] == attrs.pop("password2"):
            key_error = "invalid_re_password"
            raise serializers.ValidationError(
                {"password2": self.error_messages[key_error]}, code=key_error
            )

        return attrs


class AccountActivationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        "invalid_config": "The URL path must contain 'uidb64' and 'token' parameters.",
        "invalid_uid": "Invalid user.",
        "invalid_token": "Invalid activation token.",
    }

    def validate(self, attrs: dict) -> dict:
        if "uidb64" not in attrs or "token" not in attrs:
            key_error = "invalid_config"
            raise ImproperlyConfigured(self.error_messages[key_error])

        self.user = self.get_user(attrs["uidb64"])
        token = attrs["token"]

        if self.user is not None:
            if self.context["view"].token_generator.check_token(
                self.user, token
            ):
                return attrs

        key_error = "invalid_token"
        raise serializers.ValidationError(
            {"token": self.error_messages[key_error]}, code=key_error
        )

    def get_user(self, uidb64: str) -> User | None:
        try:
            uidb64 = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uidb64)
        except (ObjectDoesNotExist, ValueError, TypeError, OverflowError):
            user = None
            key_error = "invalid_uid"
            raise serializers.ValidationError(
                {"uid": self.error_messages[key_error]}, code=key_error
            )
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    default_error_messages = {
        "email_no_exists": "Username with that email does not exists."
    }

    def validate_email(self, email: str) -> str:
        print("jestem w validate email")
        if not User.objects.filter(email=email).exists():
            key_error = "email_no_exists"
            raise serializers.ValidationError(
                {"email": self.error_messages[key_error]}, code=key_error
            )

        return email

    def create_token(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        ForgotPasswordToken.objects.filter(user=user).delete()
        token = ForgotPasswordToken.objects.create(user=user)
        return token


class PasswordRetypeSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    password2 = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    default_error_messages = {
        "invalid_re_password": "Password fields must be the same"
    }

    class Meta:
        fields = ["password2", "password"]

    def validate(self, attrs: dict) -> dict:
        if not attrs["password"] == attrs.pop("password2"):
            key_error = "invalid_re_password"
            raise serializers.ValidationError(
                {"password2": self.error_messages[key_error]}, code=key_error
            )

        return super().validate(attrs)


class EmailAndTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(max_length=5, required=True)

    default_error_messages = {"invalid": "Token or email is invalid"}

    def validate(self, attrs: dict) -> dict:
        attrs = super().validate(attrs)
        email = attrs["email"]
        token_from_request = attrs["token"]

        try:
            self.user = User.objects.get(email=email)
            token_from_db = ForgotPasswordToken.objects.get(
                user=self.user
            ).token
            if token_from_request != token_from_db:
                raise serializers.ValidationError
        except (ObjectDoesNotExist, serializers.ValidationError):
            key_error = "invalid"
            raise serializers.ValidationError(
                {"invalid": self.error_messages[key_error]}, code=key_error
            )

        return attrs

    def delete_user_tokens(self, user: User) -> None:
        ForgotPasswordToken.objects.filter(user=user).delete()


class ForgotPasswordConfirmSerializer(
    EmailAndTokenSerializer, PasswordRetypeSerializer
):
    pass
