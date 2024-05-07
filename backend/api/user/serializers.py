from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured


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
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    default_error_messages = {
        "unique_email": "User with that email already exists",
        "invalid_re_password": "Password fields must be the same",
    }

    email = serializers.EmailField(required=True)
    password2 = serializers.CharField(required=True, write_only=True)

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
    default_error_messages = {
        "invalid_config": "The URL path must contain 'uidb64' and 'token' parameters.",
        "invalid_uid": "Invalid user.",
        "invalid_token": "Invalid activation token.",
    }

    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs: dict) -> dict:
        if "uidb64" not in attrs or "token" not in attrs:
            key_error = "invalid_config"
            raise ImproperlyConfigured(self.error_messages[key_error])

        self.user = self.get_user(attrs["uidb64"])
        token = attrs["token"]

        if self.user is not None:
            if default_token_generator.check_token(self.user, token):
                return attrs

        key_error = "invalid_token"
        raise serializers.ValidationError(
            {"token": self.error_messages[key_error]}, code=key_error
        )

    def get_user(self, uidb64):
        try:
            uidb64 = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uidb64)
        except (ObjectDoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise serializers.ValidationError(
                {"uid": self.error_messages[key_error]}, code=key_error
            )
        return user
