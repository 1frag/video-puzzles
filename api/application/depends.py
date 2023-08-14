from typing import Annotated
from uuid import UUID

from fastapi import Header, Depends

from api.domain.jwt import decode_access_token


def _get_user_id(authorization: str = Header(...)) -> UUID:
    return UUID(decode_access_token(authorization)['user_id'])


user_id = Annotated[UUID, Depends(_get_user_id)]
