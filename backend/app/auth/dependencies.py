"""FastAPI dependencies for authentication and rate limiting."""
from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.auth.rate_limit import RateLimiter
from backend.app.auth.security import verify_access_token
from backend.app.core.settings import settings


bearer_scheme = HTTPBearer(auto_error=False)


def _get_rate_limiter(request: Request) -> RateLimiter:
    limiter = getattr(request.app.state, "rate_limiter", None)
    if isinstance(limiter, RateLimiter):
        return limiter
    limiter = RateLimiter(
        max_requests=settings.rate_limit_requests_per_minute,
        window_seconds=settings.rate_limit_window_seconds,
    )
    request.app.state.rate_limiter = limiter
    return limiter


def rate_limit_request(request: Request) -> None:
    """Apply a simple per-client rate limit."""

    limiter = _get_rate_limiter(request)
    identity = request.client.host if request.client else "anonymous"
    allowed, retry_after = limiter.allow(identity)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": "RATE_LIMITED",
                "message": "Too many requests. Please try again later.",
                "retry_after_seconds": retry_after,
            },
            headers={"Retry-After": str(retry_after)},
        )


def require_request_access(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> None:
    """Enforce JWT authentication when enabled in settings."""

    if not settings.require_auth:
        return

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "AUTH_REQUIRED", "message": "Bearer token required."},
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        claims = verify_access_token(token, settings.jwt_secret.get_secret_value())
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_TOKEN", "message": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    request.state.auth_claims = claims