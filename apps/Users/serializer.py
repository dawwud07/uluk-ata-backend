from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import OTPCode, User
from .otp_services import get_valid_otp, otp_error_response


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key, "email": user.email}


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True, min_length=6, max_length=6)

    class Meta:
        model = User
        fields = [
            "email",
            "code",
            "password",
            "password2",
            "first_name",
            "last_name",
            "phone",
            "date_of_birth",
            "gender",
            "avatar",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        otp, error = get_valid_otp(attrs["email"], attrs["code"])
        error_response = otp_error_response(error)
        if error_response:
            raise serializers.ValidationError({"code": error_response.data["error"]})
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "User with this email already exists."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2", None)
        code = validated_data.pop("code", None)
        user = User.objects.create_user(**validated_data)
        OTPCode.objects.filter(email=user.email, code=code).delete()
        token, _ = Token.objects.get_or_create(user=user)
        user._token_key = token.key
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "date_of_birth",
            "gender",
        )
        read_only_fields = ("email", "phone")

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            data = data.dict()
        return super().to_internal_value(data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    def validate(self, attrs: dict):
        user: User = self.context["request"].user
        if not user.check_password(attrs.get("old_password")):
            raise serializers.ValidationError("The current password is incorrect.")
        if attrs.get("old_password") == attrs.get("new_password"):
            raise serializers.ValidationError(
                "The new password must differ from the current password."
            )
        return attrs

    def save(self, **kwargs):
        user: User = self.context["request"].user
        user.set_password(self.validated_data.get("new_password"))
        user.save()
        return user


class DeactivateSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)
    new_password = serializers.CharField(min_length=8)
