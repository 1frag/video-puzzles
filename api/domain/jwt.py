import datetime
from uuid import UUID

import jwt

from api.settings import settings


def create_access_token(user_id: UUID) -> str:
    return jwt.encode(
        {
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
            'user_id': str(user_id),
        },
        settings.jwt_secret,
        algorithm='HS256'
    )


def decode_access_token(access_token: str) -> dict:
    return jwt.decode(
        jwt=access_token,
        key=settings.jwt_secret,
        algorithms=['HS256'],
    )
