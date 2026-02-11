import json
from typing import Optional
from app.core.redis import redis_client


def get_cache(key: str) -> Optional[dict]:
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except Exception:
        return None


def set_cache(key: str, value: dict, ttl: int):
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception:
        pass


def invalidate_cache(*keys: str):
    try:
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass
