from rest_framework import serializers, exceptions, status
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from collections import OrderedDict


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
            },
        }

    # def validate(self, attrs: dict) -> dict:
    #     print("jestem w validate")
    #     errors = []
    #     try:
    #         validate_password(attrs["password"])
    #     except ValidationError as error:
    #         errors.append(error)

    #     try:
    #         if not attrs["password"] == attrs.pop("password2"):
    #             error_message = {
    #                 "password": "Password fields must be the same"
    #             }
    #             raise ValidationError(error_message)
    #     except ValidationError as error:
    #         errors.append(error)

    #     if errors:
    #         raise ValidationError(errors)
    #     return attrs

    def validate(self, attrs: dict) -> dict:
        if not attrs["password"] == attrs.pop("password2"):
            error_message = "Password fields must be the same"
            raise serializers.ValidationError(
                {"error": error_message, "status": status.HTTP_400_BAD_REQUEST}
            )

    def validate_email(self, email: str) -> str:
        print("jestem w validate_email")
        if User.objects.filter(email=email).exists():
            error_message = "User with that email already exists"
            raise serializers.ValidationError(
                {"error": error_message, "status": status.HTTP_400_BAD_REQUEST}
            )

        return email

    # def is_valid(self, *, raise_exception=False):
    #     assert hasattr(self, "initial_data"), (
    #         "Cannot call `.is_valid()` as no `data=` keyword argument was "
    #         "passed when instantiating the serializer instance."
    #     )
    #     # print("w is valid")
    #     if not hasattr(self, "_validated_data"):
    #         try:
    #             # print("w is valid w bloku try")
    #             self._validated_data = self.run_validation(self.initial_data)
    #             # print("w is valid w bloku try zaraz przede except")
    #         except serializers.ValidationError as exc:
    #             # print("w is valid w bloku try ale w except")
    #             self._validated_data = {}
    #             self._errors = exc.detail
    #         else:
    #             # print("w is valid w bloku try ale w else")
    #             self._errors = {}

    #     # print("w is valid zaraz przed raise validationerror")
    #     print("errors w is_valid: ", self._errors)
    #     if self._errors and raise_exception:
    #         raise serializers.ValidationError(self.errors)

    #     return not bool(self._errors)

    # def run_validation(self, data=serializers.empty):
    #     """
    #     We override the default `run_validation`, because the validation
    #     performed by validators and the `.validate()` method should
    #     be coerced into an error dictionary with a 'non_fields_error' key.
    #     """
    #     print("jestem w run_validation")
    #     (is_empty_value, data) = self.validate_empty_values(data)
    #     if is_empty_value:
    #         return data

    #     value = self.to_internal_value(data)
    #     try:
    #         self.run_validators(value)
    #         value = self.validate(value)
    #         assert (
    #             value is not None
    #         ), ".validate() should return the validated data"
    #     except (serializers.ValidationError, ValidationError) as exc:
    #         raise serializers.ValidationError(
    #             detail=serializers.as_serializer_error(exc)
    #         )

    #     return value

    def to_internal_value(self, data):
        errors = OrderedDict()
        try:
            return super().to_internal_value(data)
        except (serializers.ValidationError, ValidationError) as exc:
            errors.setdefault("errors", [])
            for error in exc.detail.values():
                if not isinstance(error, dict):
                    error = {
                        "error": error[0],
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                errors["errors"].append(error)
            raise serializers.ValidationError(errors)
