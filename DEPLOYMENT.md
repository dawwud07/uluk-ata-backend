# Deployment

## Local development

When `DJANGO_DEBUG` is not set, the project uses development settings: SQLite, an in-memory Channels layer, and a development-only secret key. Start the server with `python manage.py runserver`. Do not use these defaults in production; explicitly set `DJANGO_DEBUG=False` and configure `DJANGO_SECRET_KEY`, `DATABASE_URL`, and `REDIS_URL`.

## Docker Compose

1. Copy `.env.example` to `.env` and replace the Django secret, database password, host names, and email settings. Keep `.env` out of version control.
2. Set `DATABASE_URL` to the same database, user, and password configured in the `POSTGRES_*` variables. URL-encode special characters in the password.
3. Run `docker compose up --build`.

The web container applies migrations, collects static files, and serves HTTP and WebSockets with Daphne. PostgreSQL stores application data, Redis carries Channels events, and uploaded files use a persistent Docker volume. Terminate TLS at a trusted reverse proxy and forward `X-Forwarded-Proto: https`; configure `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `CORS_ALLOWED_ORIGINS` for the deployed domain.

## WebSocket notifications

Connect at `wss://<host>/ws/notifications/` using the Django session cookie or the API token returned by the existing login endpoint as the `token` query parameter. Use TLS and configure proxy/access logs not to record query strings when token authentication is used. The endpoint accepts no application messages; it sends JSON notification objects when a new notification is created for that user.

## Before production

- Rotate credentials previously configured in source and set fresh values in `.env` or the deployment secret manager.
- Resolve the outstanding model/migration drift reported by `python manage.py makemigrations --check --dry-run` for `Users` and `Restaurant` before applying new migrations. Review any generated migration for data impact.
- Run the full test suite and `python manage.py check --deploy` in the production environment.
- Configure TLS, backups for PostgreSQL and uploaded media, monitoring, and a deployment-specific health check.