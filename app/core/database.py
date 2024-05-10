from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from .config import settings


def init_db(app: FastAPI):
    Tortoise.init_models(["app.users.models", "app.posts.models"], "models")
    register_tortoise(
        app,
        db_url=settings.db.DB_URI,
        modules={"models": ["app.users.models", "app.posts.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


TORTOISE_ORM = {
    "connections": {"default": settings.db.DB_URI},
    "apps": {
        "models": {
            "models": ["app.users.models", "app.posts.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
