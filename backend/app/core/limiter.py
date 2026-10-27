"""Small in-memory limiter for public submissions and login attempts."""

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status


class RateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str, limit: int, window_seconds: int) -> bool:
        now = time.monotonic()
        bucket = self._hits[key]
        while bucket and now - bucket[0] > window_seconds:
            bucket.popleft()
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True

    def reset(self) -> None:
        self._hits.clear()


limiter = RateLimiter()


def client_key(request: Request) -> str:
    if request.client is None:
        return "unknown"
    return request.client.host


def enforce_limit(request: Request, bucket: str, limit: int, window_seconds: int) -> None:
    if not limiter.allow(f"{bucket}:{client_key(request)}", limit, window_seconds):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Zu viele Anfragen. Bitte versuchen Sie es später erneut.",
        )
