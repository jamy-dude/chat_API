from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from channels.middleware import BaseMiddleware


@database_sync_to_async
def get_user(token_key):
    try:
        print(f'token_key: {token_key}')
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            auth_header = headers[b'authorization'].decode()
            print(f"Auth header received: {auth_header}")

        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            print(f"Token key received: {token_key} and Token name: {token_name}")
        #token_key = scope['query_string'].decode().split('=')[-1]

        print(f'token_key in TokenAuthMiddleware: {token_key}')
        print(f'headers in TokenAuthMiddleware: {headers}')

        scope['user'] = await get_user(token_key)

        return await super().__call__(scope, receive, send)
