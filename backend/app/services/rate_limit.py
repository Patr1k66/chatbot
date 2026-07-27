import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from app.config import settings


class RateLimiter:
    def __init__(self, limit: int, window_seconds: int = 60) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.time()
        bucket = self._requests[key]

        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.limit:
            raise HTTPException(
                status_code=429,
                detail="Слишком много запросов. Попробуйте через минуту.",
            )

        bucket.append(now)


rate_limiter = RateLimiter(settings.rate_limit_per_minute)


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"
