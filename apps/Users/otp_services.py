from rest_framework import status
from rest_framework.response import Response

from .models import OTPCode


def get_valid_otp(email: str, code: str):
    """
    Look up an OTP code by email and code, and check expiry.

    Returns:
        (OTPCode, None) on success.
        (None, 'not_found') when no matching code exists.
        (None, 'expired') when the code exists but is expired (deleted).
    """
    otp = OTPCode.objects.filter(email=email, code=code).first()
    if otp is None:
        return None, "not_found"
    if otp.is_expired():
        otp.delete()
        return None, "expired"
    return otp, None


def otp_error_response(error: str):
    """Return a DRF Response for a failed OTP validation, or None."""
    if error == "not_found":
        return Response(
            {"error": "Request a verification code first."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if error == "expired":
        return Response(
            {"error": "Verification code has expired. Request a new one."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return None
