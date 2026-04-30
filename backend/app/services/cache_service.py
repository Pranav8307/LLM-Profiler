# app/services/cache_service.py

import redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class CacheService:
    def __init__(self):
        self.client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

    def get(self, key: str):
        value = self.client.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value, ttl: int = 300):
        self.client.setex(key, ttl, json.dumps(value))

    def make_key(self, prompt: str, model: str):
        return f"llm:{model}:{hash(prompt)}"