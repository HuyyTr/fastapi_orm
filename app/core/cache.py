from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from .config import settings


def init_cache():
    redis = aioredis.from_url(
        url=settings.cache.REDIS_URI
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
