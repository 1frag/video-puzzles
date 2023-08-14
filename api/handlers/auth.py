from fastapi import APIRouter

router = APIRouter(tags=['auth'])


@router.get('/hello')
async def root():
    return {'message': 'Hello World'}
