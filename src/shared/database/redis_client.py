import os
import redis
from src.core.config import settings


def get_redis_client():
    if settings.REDIS_URL:
        return redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
    )