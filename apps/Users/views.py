from rest_framework import generics, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializer import (
    ChangePasswordSerializer,
    DeactivateSerializer,
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"token": user._token_key, "email": user.email},
            status=status.HTTP_201_CREATED,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {
                    "is_guest": True,
                    "message": "Log in to save addresses and profile details.",
                }
            )

        return super().retrieve(request, *args, **kwargs)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password changed successfully."})


class DeactivateView(generics.GenericAPIView):
    serializer_class = DeactivateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.validated_data.get("confirm"):
            raise serializers.ValidationError(
                {"confirm": ["Confirm account deactivation."]}
            )

        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"detail": "Account deactivated successfully."}, status=status.HTTP_200_OK
        )


class LogoutView(generics.GenericAPIView):
    serializer_class = serializers.Serializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response(
            {"detail": "You have been logged out successfully."},
            status=status.HTTP_200_OK,
        )
