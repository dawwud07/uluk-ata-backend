from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('nepravilen email ili lozinka')

        token, _ = Token.objects.get_or_create(user=user)
        return {"token": token.key, "email": user.email}


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'date_of_birth', 'avatar'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "paroli se ne sovpadaat"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = User.objects.create_user(**validated_data)
        Token.objects.get_or_create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "avatar", "phone", "date_of_birth")
        read_only_fields = ("email",)

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            data = data.dict()
        return super().to_internal_value(data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs: dict):
        user: User = self.context["request"].user
        if not user.check_password(attrs.get("old_password")):
            raise serializers.ValidationError("Неверный старый пароль.")
        if attrs.get("old_password") == attrs.get("new_password"):
            raise serializers.ValidationError("Новый пароль не может совпадать со старым.")
        return attrs

    def save(self, **kwargs):
        user: User = self.context["request"].user
        user.set_password(self.validated_data.get("new_password"))
        user.save()
        return user


class DeactivateSeriliazer(serializers.Serializer):
    confirm = serializers.BooleanField()




class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    
    
class ResetPasswordSerilizer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length = 6 , max_length = 6)
    new_password = serializers.CharField(min_length= 8)
