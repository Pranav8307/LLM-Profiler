# app/services/rate_limiter.py

import time
import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class RateLimiter:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL)

    def is_allowed(self, user_id: str, limit: int = 10, window: int = 60):
        """
        limit = requests
        window = seconds
        """
        key = f"rate:{user_id}"

        current = self.client.get(key)

        if current is None:
            self.client.set(key, 1, ex=window)
            return True

        if int(current) >= limit:
            return False

        self.client.incr(key)
        return True