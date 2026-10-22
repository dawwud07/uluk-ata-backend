from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "apps.Users"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        import os

        import firebase_admin
        from django.conf import settings
        from firebase_admin import credentials

        try:
            firebase_admin.get_app()
        except ValueError:
            pass
        else:
            # Firebase app already initialised.
            return

        cred_path = getattr(
            settings,
            "FIREBASE_CREDENTIALS_PATH",
            os.path.join(
                settings.BASE_DIR, "apps", "firebase", "serviceAccountKey.json"
            ),
        )
        if cred_path and not os.path.isabs(str(cred_path)):
            cred_path = os.path.join(settings.BASE_DIR, str(cred_path))
        if not cred_path or not os.path.exists(str(cred_path)):
            return
        cred = credentials.Certificate(str(cred_path))
        firebase_admin.initialize_app(cred)
