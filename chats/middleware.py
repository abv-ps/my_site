from typing import Optional

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        token = Token.objects.select_related('user').get(key=token_key)
        print(f"Authenticated user: {token.user}")
        return token.user
    except:
        print("Token not found")
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom middleware for token-based authentication using DRF tokens.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        headers = dict(scope.get('headers', []))
        cookie_header = headers.get(b"cookie", b"")
        print("Incoming headers:", headers)

        token_key: Optional[str] = None

        if cookie_header:
            cookies = cookie_header.decode('utf-8').split(';')
            for cookie in cookies:
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    if key == 'token':
                        token_key = value
                        break

        if token_key:
            print(f"Token key: {token_key}")
            scope["user"] = await get_user_from_token(token_key)
        else:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
