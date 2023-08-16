from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .application.lifespan import lifespan
from .application.middlewares.postgres import init_postgres_connection
from .handlers import auth, puzzles


def create_app(include_static: bool):
    app = FastAPI(lifespan=lifespan)
    app.include_router(auth.router, prefix='/api/auth')
    app.include_router(puzzles.router, prefix='/api/puzzles')
    app.middleware('http')(init_postgres_connection)
    if include_static:
        app.mount('/', StaticFiles(directory='www/'), 'www')
    return app
