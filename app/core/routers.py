from fastapi import FastAPI

from app.users.api import users_router
from app.posts.api import posts_router

from .config import settings


def init_routers(app: FastAPI):
    app.include_router(users_router, prefix=settings.environment.API_PREFIX)
    app.include_router(posts_router, prefix=settings.environment.API_PREFIX)
