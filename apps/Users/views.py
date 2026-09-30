from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import OTPCode, User


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
                'message': 'Log in to save addresses and profile details.',
            })

        return super().retrieve(request, *args, **kwargs)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
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
            raise serializers.ValidationError({"confirm": ["Confirm account deactivation."]})

        user = request.user
        user.is_active = False
        user.save()
        return Response({"detail": "Account deactivated successfully."}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "You have been logged out successfully."}, status=status.HTTP_200_OK)


class RegisterVerifyView(APIView):
    def post(self, request):
        email = request.data["email"]
        code = request.data["code"]
        password = request.data["password"]

        otp = OTPCode.objects.filter(email=email, code=code).first()

        if otp is None:
            return Response({"detail": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        if otp.is_expired():
            otp.delete()
            return Response({"detail": "Verification code has expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        otp.delete()

        return Response({"token": token.key})
