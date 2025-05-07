from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

@database_sync_to_async
def get_user_from_token(token_key):
    try:
        token = Token.objects.select_related('user').get(key=token_key)
        return token.user
    except:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['user'] = AnonymousUser()

        headers = dict(scope.get('headers',[]))

        token_key = None

        if not token_key:
            cookie_header = headers.get(b'cookie')
            if cookie_header:
                cookies = cookie_header.decode('utf-8').split(';')
                for cookie in cookies:
                    if '=' in cookie:
                        key, value = cookie.strip.split('=', 1)
                        if key == 'token':
                            token_key = value
                            break

        if token_key:
            print(f"Token key: {token_key}")
            scope['user'] = await get_user_from_token(token_key)

        return await super().__call__(scope, receive, send)

