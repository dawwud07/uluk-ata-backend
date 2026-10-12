from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user_from_token(key):
    try:
        user = Token.objects.select_related('user').get(key=key).user
    except Token.DoesNotExist:
        return AnonymousUser()
    return user if user.is_active else AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode('ascii', errors='ignore')
        token = parse_qs(query_string).get('token', [None])[0]
        if token:
            scope = {**scope, 'user': await get_user_from_token(token)}
        return await self.inner(scope, receive, send)