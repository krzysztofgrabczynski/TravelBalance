from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from api.user.models import MyUser
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import (
    ObjectDoesNotExist,
    ImproperlyConfigured,
    PermissionDenied,
)

from api.user.models import ForgotPasswordToken, FeedbackFromUser


User = get_user_model()


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
        "password_mismatch": "Password fields must be the same"
    }

    def validate(self, attrs: dict) -> dict:
        if not attrs["password"] == attrs.pop("password2"):
            key_error = "password_mismatch"
            raise serializers.ValidationError(
                self.error_messages[key_error], code=key_error
            )

        return super().validate(attrs)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, style={"input_type": "password"}
    )

    default_error_messages = {
        "invalid_credentials": "Invalid credentials.",
        "user_inactive": "User is not active.",
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
                self.error_messages[key_error], code=key_error
            )
        except ObjectDoesNotExist:
            key_error = "invalid_credentials"
            raise serializers.ValidationError(
                self.error_messages[key_error], code=key_error
            )

    def _create_user_auth_token(self, user: MyUser) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
        extra_kwargs = {
            "email": {"validators": [UniqueValidator(User.objects.all())]},
        }


class UserCreateSerializer(
    PasswordRetypeSerializer, serializers.ModelSerializer
):
    email = serializers.EmailField(required=True)

    default_error_messages = {
        "unique_email": "User with that email already exists",
    }

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate_email(self, email: str) -> str:
        if User.objects.filter(email=email).exists():
            key_error = "unique_email"
            raise serializers.ValidationError(
                self.error_messages[key_error], code=key_error
            )

        return email

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class AccountActivationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    default_error_messages = {
        "invalid_config": "The URL path must contain 'uidb64' and 'token' parameters.",
        "user_activation_error": "User activation error.",
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

        key_error = "user_activation_error"
        raise serializers.ValidationError(
            self.error_messages[key_error], code=key_error
        )

    def get_user(self, uidb64: str) -> MyUser | None:
        try:
            uidb64 = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uidb64)
        except (ObjectDoesNotExist, ValueError, TypeError, OverflowError):
            user = None
        return user


class PasswordResetSerializer(PasswordRetypeSerializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"},
    )

    default_error_messages = {
        "wrong_old_password": "Old password is incorrect."
    }

    def validate_old_password(self, old_password: str) -> str:
        self.user = self.context["request"].user
        if self.user.check_password(old_password):
            return old_password
        key_error = "wrong_old_password"
        raise serializers.ValidationError(
            self.error_messages[key_error], code=key_error
        )


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    default_error_messages = {
        "email_no_exists": "Username with that email does not exists."
    }

    def validate_email(self, email: str) -> str:
        if not User.objects.filter(email=email).exists():
            key_error = "email_no_exists"
            raise serializers.ValidationError(
                self.error_messages[key_error], code=key_error
            )

        return email

    def create_token(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        ForgotPasswordToken.objects.filter(user=user).delete()
        token = ForgotPasswordToken.objects.create(user=user)
        return token


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
                self.error_messages[key_error], code=key_error
            )

        return attrs

    def delete_user_tokens(self, user: MyUser) -> None:
        ForgotPasswordToken.objects.filter(user=user).delete()


class ForgotPasswordConfirmSerializer(
    EmailAndTokenSerializer, PasswordRetypeSerializer
):
    pass


class FeedbackFromUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FeedbackFromUser
        fields = ("user", "message", "type")
