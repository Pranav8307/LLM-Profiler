import redis
from app.core.config import get_settings

settings = get_settings()

# Module-level client — reused across requests
redis_client = redis.from_url(
    settings.redis_url,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
)


def get_redis() -> redis.Redis:
    """
    FastAPI dependency.
    Usage:
        cache: Redis = Depends(get_redis)
    """
    return redis_client


def check_redis_connection() -> bool:
    """Used by health check endpoint."""
    try:
        return redis_client.ping()
    except Exception:
        return False