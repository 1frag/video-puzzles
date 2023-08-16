import json

from fastapi import APIRouter, Response

from api.domain.tokens import create_access_token
from api.domain.models.next_action import NextAction
from api.integrations.google import get_link_to_auth, get_access_token, get_user_info
from api.integrations.postgres.users import add_user, update_google_email, get_user

router = APIRouter(tags=['auth'])


@router.post('/google/login')
async def google_login(
        next_action: NextAction,
):
    """
    Начало авторизации через гугл.
    Надо запомнить цель пользователя (что он хотел сделать перед авторизацией)
    после успешной авторизации продолжить действие имея jwt токен
    """
    url, request_id = get_link_to_auth()
    await add_user(request_id, next_action)
    return {
        'url': url,
    }


@router.get('/google/redirect')
async def google_redirect(code: str, state: str):
    google_access_token = await get_access_token(code)
    user_info = await get_user_info(google_access_token)
    existed_user_id = await get_user(user_info.email)

    if existed_user_id:
        user_id, next_action = existed_user_id, None
    else:
        user_id, next_action = await update_google_email(state, user_info.email, user_info.name)

    access_token = create_access_token(user_id)

    meta = 'const _META = ' + json.dumps({
        'user_id': str(user_id),
        'name': user_info.name,
        'next_action': next_action,
        'access_token': access_token,
    })
    return Response(
        content=f'''
            <html>
            <head><title>Loading...</title></head>
            <body>
                <script>{meta}</script>
                <script src="/_google-redirect.js"></script>
            </body>
            </html>
        ''',
        media_type='text/html',
    )
