from fastapi import APIRouter

from api.application import depends
from api.domain.models.verifing_game import VerifyingGame
from api.integrations.postgres.results import add_result, get_leaders
from api.integrations.postgres.users import update_nickname

router = APIRouter()


@router.post('/verify', status_code=204)
async def verify_game(user_id: depends.user_id, data: VerifyingGame):
    """
    Потенциально тут можно добавить различные проверки, что пользователь в действительности собрал пазлы, а не
    использовал js для этого или вообще просто отправил запрос напрямую
    """
    await update_nickname(user_id, data.name)
    await add_result(user_id, data.duration_secs)


@router.get('/leaderboard/{puzzle_id}')
async def verify_game(puzzle_id: str):
    leaders = await get_leaders(puzzle_id)
    return {
        'leaders': leaders
    }
