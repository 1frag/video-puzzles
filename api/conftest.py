import asyncpg
import pytest_asyncio

from api.application.state import state
from api.settings import settings


@pytest_asyncio.fixture()
async def pg_pool():
    async with asyncpg.create_pool(settings.postgres_dsn) as _pg_pool:
        state.get().pg_pool = _pg_pool
        yield _pg_pool


@pytest_asyncio.fixture()
async def pg_connection(pg_pool):
    async with pg_pool.acquire() as _pg_connection:
        state.get().pg_connection = _pg_connection
        yield _pg_connection
