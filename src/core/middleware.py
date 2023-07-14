from django.conf import settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode
from urllib.parse import parse_qs
from users.models import User

from channels.db import database_sync_to_async


@database_sync_to_async
def get_user_from_db(user_id: str) -> None | User:
    """Get user by its user_id."""
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None


class TokenAuthMiddleware:
    """Token authentication middleware for channels."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        query_string_parse = parse_qs(query_string)
        token = query_string_parse['token'][0]

        try:
            is_valid = UntypedToken(token)
        except (InvalidToken, TokenError):
            scope["user"] = None
            return

        else:
            user_data = decode(
                jwt=token,
                key=settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithms=[settings.SIMPLE_JWT['ALGORITHM']]
            )
            user = await get_user_from_db(user_data['user_id'])
            scope['user'] = user

        return await self.app(scope, receive, send)
