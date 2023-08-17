from uuid import UUID

from api.application.state import state
from api.integrations.postgres.models.leader import Leader


async def add_result(
        user_id: UUID,
        puzzle_id: str,
        duration_secs: int,
) -> None:
    await state.get().pg_connection.execute(
        '''
            INSERT INTO user_results (user_id, puzzle_id, duration_secs)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id, puzzle_id) DO UPDATE SET duration_secs = $3
        ''',
        user_id,
        puzzle_id,
        duration_secs,
    )


async def get_leaders(puzzle_id: str) -> list[Leader]:
    rows = await state.get().pg_connection.fetch(
        '''
            SELECT u.name, r.duration_secs
            FROM user_results r
            INNER JOIN users u on u.id = r.user_id
            WHERE r.puzzle_id = $1
            ORDER BY r.duration_secs
            LIMIT 5
        ''',
        puzzle_id,
    )
    return [
        Leader(
            name=row['name'],
            duration_secs=row['duration_secs'],
        ) for row in rows
    ]
