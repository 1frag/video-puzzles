import pytest

from api.domain.models.next_action import NextAction, NextActionIdent
from api.integrations.postgres.users import add_user

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_add_user(pg_connection):
    await add_user('123', NextAction(ident=NextActionIdent.PUBLISH_RESULT))
