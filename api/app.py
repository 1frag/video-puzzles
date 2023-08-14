from fastapi import FastAPI

from .application.lifespan import lifespan
from .application.middlewares.postgres import init_postgres_connection
from .handlers import auth, game


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(auth.router, prefix='/api/auth')
    app.include_router(game.router, prefix='/api/game')
    app.middleware('http')(init_postgres_connection)
    return app
