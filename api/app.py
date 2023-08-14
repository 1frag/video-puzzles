from fastapi import FastAPI

from .handlers import auth


def create_app():
    app = FastAPI()
    app.include_router(auth.router, prefix='/api/auth')
    return app
