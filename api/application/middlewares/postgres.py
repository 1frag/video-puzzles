from fastapi import Request

from api.application.state import state


async def init_postgres_connection(request: Request, call_next):
    async with state.get().pg_pool.acquire() as pg_connection:
        state.get().pg_connection = pg_connection
        return await call_next(request)
