from fastapi import FastAPI

from . import signals
from .middleware import init_middleware
from .database import init_db
from .cache import init_cache
from .routers import init_routers
from .admin import init_admin_app


def config_app(app: FastAPI) -> None:
    init_db(app)  # db
    init_cache()  # cache
    init_middleware(app)  # middleware
    init_routers(app)  # router
    init_admin_app(app)
