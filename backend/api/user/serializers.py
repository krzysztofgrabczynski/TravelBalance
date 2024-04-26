from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class UserCreateMixin:
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
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
            }
        }

    def validate(self, attrs: dict) -> dict:
        if not attrs["password"] == attrs.pop("password2"):
            error_message = {"password": "Password fields must be the same"}
            raise serializers.ValidationError(error_message)

        return super().validate(attrs)

    def validate_email(self, email: str) -> str:
        if User.objects.filter(email=email).exists():
            error_message = "User with that email already exists"
            raise serializers.ValidationError(error_message)

        return email
