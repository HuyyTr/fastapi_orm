from fastapi import FastAPI
import uvicorn

from app.users.api import users_router
from app.core.config import settings
from app.core.initalize import config_app

app = FastAPI(debug=settings.environment.DEBUG)


config_app(app)


def main(args=None):
    uvicorn.run("main:app", host=settings.host.SERVER_HOST,
                port=settings.host.SERVER_PORT, reload=True)


if __name__ == "__main__":
    main()
