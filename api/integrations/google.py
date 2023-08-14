import json

import httpx
from fastapi.exceptions import HTTPException

import google_auth_oauthlib.flow
from pydantic import BaseModel

CREDENTIALS_FILENAME = 'google-web-1.json'
CREDENTIALS = json.load(open(CREDENTIALS_FILENAME))
GOOGLE_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USER_INFO_URI = 'https://www.googleapis.com/oauth2/v1/userinfo'


class UserInfo(BaseModel):
    email: str
    name: str


def _scopes(*suffixes):
    return [f'https://www.googleapis.com/{suffix}' for suffix in suffixes]


def get_link_to_auth() -> tuple[str, str]:
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CREDENTIALS_FILENAME,
        scopes=_scopes('auth/userinfo.email', 'auth/userinfo.profile')
    )
    flow.redirect_uri = 'https://puzzle.ifrag-dev.ru/api/auth/google/redirect'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )
    return authorization_url, state


async def get_access_token(code: str) -> str:
    parameters = {
        'client_id': CREDENTIALS['web']['client_id'],
        'client_secret': CREDENTIALS['web']['client_secret'],
        'redirect_uri': CREDENTIALS['web']['redirect_uris'][0],
        'grant_type': 'authorization_code',
        'code': code,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(GOOGLE_TOKEN_URI, data=parameters)
        data = response.json()
        if access_token := data.get('access_token'):
            return access_token

        print('Unsuccessful response', data)
        if data.get('error') == 'invalid_grant':
            raise HTTPException(status_code=400)
        raise NotImplementedError


async def get_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_USER_INFO_URI, headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        return UserInfo(**response.json())
