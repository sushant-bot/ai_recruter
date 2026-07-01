"""Simple in-memory rate limiter."""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from threading import Lock
from time import time


@dataclass
class RateLimiter:
    """Track request timestamps per client identity."""

    max_requests: int
    window_seconds: int
    _requests: dict[str, deque[float]] = field(default_factory=lambda: defaultdict(deque))
    _lock: Lock = field(default_factory=Lock)

    def allow(self, identity: str, now: float | None = None) -> tuple[bool, int]:
        """Return whether the request is allowed and the retry delay in seconds."""

        current_time = time() if now is None else now
        with self._lock:
            timestamps = self._requests[identity]
            threshold = current_time - self.window_seconds
            while timestamps and timestamps[0] <= threshold:
                timestamps.popleft()

            if len(timestamps) >= self.max_requests:
                retry_after = max(1, int(self.window_seconds - (current_time - timestamps[0])))
                return False, retry_after

            timestamps.append(current_time)
            return True, 0