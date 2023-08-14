from contextlib import asynccontextmanager

import asyncpg
from fastapi import FastAPI

from api.application.state import state
from api.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with asyncpg.create_pool(settings.postgres_dsn) as pg_pool:
        state.get().pg_pool = pg_pool
        yield
        state.get().pg_pool = None
