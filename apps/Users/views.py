from rest_framework import generics, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User
import random
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token


from .serializer import (
    ChangePasswordSerializer,
    DeactivateSeriliazer,
    LoginSerializer,
    ProfileSerializer,
    RegisterSerializer,
)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({
                'is_guest': True,
                'message': 'Войдите, чтобы сохранять адреса и данные профиля.',
            })

        return super().retrieve(request, *args, **kwargs)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Пароль успешно изменен."})


class DeactivateView(generics.GenericAPIView):
    serializer_class = DeactivateSeriliazer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data.get("confirm"):
            raise serializers.ValidationError({"confirm": ["Подтвердите деактивацию аккаунта."]})

        user = request.user
        user.is_active = False
        user.save()
        return Response({"detail": "Аккаунт успешно деактивирован."}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        email = request.data["email"]
        code = f"{random.randint(100000, 999999)}"

        cache.set(f"otp:{email}", code, 300)  # 5 минут
        

        send_mail(
            "Код подтверждения",
            f"Ваш код: {code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return Response({"detail": "Код отправлен"})


class RegisterVerifyView(APIView):
    def post(self, request):
        email = request.data["email"]
        code = request.data["code"]
        password = request.data["password"]

        saved_code = cache.get(f"otp:{email}")

        if str(saved_code) != str(code):
            return Response({"detail": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})
