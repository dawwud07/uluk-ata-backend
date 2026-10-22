import random
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTPCode, User
from .otp_services import get_valid_otp, otp_error_response
from .serializer import ResetPasswordSerializer, SendOTPSerializer, VerifyOTPSerializer


class SendOTPCodeView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = str(random.randint(100000, 999999))

        otp = OTPCode.objects.create(
            email=email,
            code=code,
            expire_at=timezone.now() + timedelta(minutes=5),
            purpose="verification",
        )

        try:
            send_mail(
                subject="Verification code",
                message=f"Your verification code is: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except (OSError, TimeoutError):
            otp.delete()
            return Response(
                {
                    "error": (
                        "Could not connect to the email server. "
                        "Please try again later."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"detail": "Verification code sent."})


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        otp, error = get_valid_otp(email, code)
        error_response = otp_error_response(error)
        if error_response:
            return error_response

        return Response(
            {"message": "Verification code confirmed."}, status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        new_password = serializer.validated_data["new_password"]

        otp, error = get_valid_otp(email, code)
        error_response = otp_error_response(error)
        if error_response:
            return error_response

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_401_UNAUTHORIZED
            )

        user.set_password(new_password)
        user.save()
        otp.delete()

        return Response(
            {"message": "Password changed successfully."}, status=status.HTTP_200_OK
        )
