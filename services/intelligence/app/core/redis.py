import redis.asyncio as redis
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

class RedisClient:
    def __init__(self):
        self.redis = None

    async def connect(self):
        try:
            self.redis = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
            await self.redis.ping()
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise e

    async def close(self):
        if self.redis:
            await self.redis.close()
            logger.info("Redis connection closed")

    async def get_client(self):
        if not self.redis:
            await self.connect()
        return self.redis

    def __getattr__(self, name):
        return getattr(self.redis, name)

redis_client = RedisClient()
