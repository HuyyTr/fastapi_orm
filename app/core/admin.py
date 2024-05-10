from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.resources import Link
from app.users import models

from .config import settings

import redis.asyncio as redis

login_provider = UsernamePasswordProvider(
    admin_model=models.User,
    login_logo_url="https://preview.tabler.io/static/logo.svg"
)


def init_admin_app(app: FastAPI):
    @admin_app.register
    class Home(Link):
        label = "Home"
        icon = "fas fa-home"
        url = "/admin"

    app.mount("/admin", admin_app)
