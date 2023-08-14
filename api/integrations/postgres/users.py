from uuid import UUID

from api.application.state import state
from api.domain.models.next_action import NextAction


async def add_user(
        google_request_id: str,
        next_action: NextAction,
) -> None:
    await state.get().pg_connection.execute(
        '''
            INSERT INTO users (google_request_id, next_action)
            VALUES ($1, $2)
        ''',
        google_request_id,
        next_action.model_dump_json(),
    )


async def update_google_email(
        google_request_id: str,
        google_email: str,
        real_name: str,
) -> tuple[UUID, NextAction]:
    user_id, next_action = await state.get().pg_connection.fetchrow(
        '''
            UPDATE users
            SET google_email=$2, real_name=$3
            WHERE google_request_id=$1
            RETURNING id, next_action
        ''',
        google_request_id,
        google_email,
        real_name,
    )
    return user_id, next_action


async def update_nickname(
        user_id: UUID,
        name: str,
):
    await state.get().pg_connection.execute(
        '''
            UPDATE users
            SET name=$2
            WHERE id=$1
        ''',
        user_id,
        name,
    )


async def get_user(google_email: str) -> UUID | None:
    return await state.get().pg_connection.fetchval(
        '''
            SELECT id
            FROM users
            WHERE google_email = $1
        ''',
        google_email,
    )
