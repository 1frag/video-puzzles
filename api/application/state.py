from contextvars import ContextVar

import asyncpg


class State:
    def __init__(
            self,
            pg_pool: asyncpg.Pool | None = None,
            pg_connection: asyncpg.Connection | None = None,
    ):
        self.pg_pool = pg_pool
        self.pg_connection = pg_connection


state: ContextVar[State] = ContextVar('state', default=State())
