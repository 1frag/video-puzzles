from api.application.state import state
from api.integrations.postgres.models.puzzle import Puzzle


async def get_puzzles() -> list[Puzzle]:
    rows = await state.get().pg_connection.fetch(
        '''
            SELECT *
            FROM puzzles
        ''',
    )
    return [
        Puzzle(
            id=row['id'],
            name=row['name'],
            preview=row['preview'],
            metadata=row['metadata'],
        ) for row in rows
    ]
