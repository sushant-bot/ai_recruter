"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, Request, status

from backend.app.auth.dependencies import rate_limit_request, require_request_access
from backend.app.auth.security import create_access_token
from backend.app.core.settings import settings
from backend.app.schemas.auth import CurrentUserResponse, TokenRequest, TokenResponse


router = APIRouter(tags=["auth"], prefix="/auth", dependencies=[Depends(rate_limit_request)])


@router.post("/token", response_model=TokenResponse)
def create_token(request: TokenRequest) -> TokenResponse:
    """Issue a signed JWT for the configured service account."""

    if request.username != settings.auth_username or request.password != settings.auth_password.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "INVALID_CREDENTIALS", "message": "Invalid username or password."},
        )

    token = create_access_token(
        request.username,
        settings.jwt_secret.get_secret_value(),
        settings.access_token_expiry_minutes,
    )
    return TokenResponse(
        access_token=token,
        expires_in_minutes=settings.access_token_expiry_minutes,
        subject=request.username,
    )


@router.get("/me", response_model=CurrentUserResponse, dependencies=[Depends(require_request_access)])
def current_user(request: Request) -> CurrentUserResponse:
    """Return the authenticated identity."""

    claims = getattr(request.state, "auth_claims", None) or {}
    return CurrentUserResponse(
        subject=str(claims.get("sub", "anonymous")),
        issuer=str(claims.get("iss", "talentmind-ai")),
        issued_at=int(claims.get("iat", 0)),
        expires_at=int(claims.get("exp", 0)),
    )