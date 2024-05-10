from starlette.datastructures import Headers

from app.core.config import settings

import time

logger = settings.logger.middleware_logger


class TimingMiddleware:
    def __init__(self, app, log):
        self.app = app
        self.log = log

    async def __call__(self, scope, receive, send):
        if self.log:
            logger.info(f"Request: {scope}")
        start_time = time.time()
        await self.app(scope, receive, send)
        duration = time.time() - start_time
        if self.log:
            logger.info(f"Request duration: {duration:.2f} seconds")
