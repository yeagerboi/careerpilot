"""
Upstash Redis Cache Helpers — CareerPilot

Cache key pattern : jobs:{md5(query+location)}
TTL              : 7200 seconds (2 hours)

Always import from here — never re-initialise Redis elsewhere.
"""

import hashlib
import json
from upstash_redis import Redis

redis = Redis.from_env()

_TTL = 7200  # 2 hours


def _job_cache_key(query: str, location: str = "") -> str:
    raw = (query + location).encode("utf-8")
    return f"jobs:{hashlib.md5(raw).hexdigest()}"


async def get_cached_jobs(query: str, location: str = "") -> list[dict] | None:
    """Return cached job list or None if cache miss."""
    key = _job_cache_key(query, location)
    value = redis.get(key)
    if value is None:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


async def cache_jobs(jobs: list[dict], query: str, location: str = "") -> None:
    """Store job list in cache with 2-hour TTL."""
    key = _job_cache_key(query, location)
    redis.set(key, json.dumps(jobs), ex=_TTL)
