from django.conf import settings
from django.contrib.auth import get_user_model
from firebase_admin import auth as firebase_auth
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class FirebaseAuthentication(BaseAuthentication):
    """Accepts `Authorization: Bearer <Firebase ID token>`.

    Verifies the Firebase ID token, then looks up (or creates) a local
    ``User`` by the verified email address and returns it.
    """

    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return None

        id_token = header[7:].strip()
        if not id_token:
            return None

        try:
            decoded = firebase_auth.verify_id_token(
                id_token,
                check_revoked=getattr(settings, "FIREBASE_CHECK_REVOKED", False),
            )
        except Exception as exc:  # noqa: BLE001 - any Firebase error is auth failure
            raise AuthenticationFailed(f"Invalid Firebase token: {exc}")

        email = (decoded.get("email") or "").strip().lower()
        if not email:
            raise AuthenticationFailed("Firebase token has no email.")

        User = get_user_model()
        first_name = (decoded.get("name") or "").split(" ")[0][:150]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "is_active": True,
            },
        )

        # Refresh the name on every successful auth so it stays in sync.
        if not created and first_name and user.first_name != first_name:
            user.first_name = first_name
            user.save(update_fields=["first_name"])

        if not user.is_active:
            raise AuthenticationFailed("User is deactivated.")

        return (user, None)
