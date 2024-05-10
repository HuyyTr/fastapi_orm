from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

import logging
from logging import Logger
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class ModelConfigBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_ignore_empty=True,
        extra="ignore"
    )


class EvironmentSettings(ModelConfigBaseSettings):  # env
    DEBUG: bool
    API_VERSION: str

    @computed_field
    @property
    def API_PREFIX(self) -> str:
        return f"/api/{self.API_VERSION}"


class LoggerSetings(ModelConfigBaseSettings):
    uvicorn_logger: Logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.addHandler(logging.StreamHandler())

    middleware_logger: Logger = logging.getLogger("middleware")
    middleware_logger.setLevel(logging.INFO)
    # todo add formater for logger
    middleware_logger.addHandler(logging.StreamHandler())


class HostSettings(ModelConfigBaseSettings):  # host
    SERVER_HOST: str
    SERVER_PORT: int


class DatabaseSettings(ModelConfigBaseSettings):     # db
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int

    @computed_field
    @property
    def DB_URI(self) -> str:
        return f"postgres://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class CacheSettings(ModelConfigBaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    @computed_field
    @property
    def REDIS_URI(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class MiddlewareSettings(BaseSettings):
    MIDDLEWARE: list = [
        {
            "type": "fastapi.middleware.cors.CORSMiddleware",
            "params": {
                "allow_origins": ["*"],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"]
            }
        },
        {
            "type": "app.middlewares.timing.TimingMiddleware",
            "params": {
                "log": False,
            }
        },
    ]


class Settings(ModelConfigBaseSettings):
    environment: EvironmentSettings = EvironmentSettings()
    logger: LoggerSetings = LoggerSetings()
    host: HostSettings = HostSettings()
    db: DatabaseSettings = DatabaseSettings()
    cache: CacheSettings = CacheSettings()
    middlware: MiddlewareSettings = MiddlewareSettings()


settings = Settings()
