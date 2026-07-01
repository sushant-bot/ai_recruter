"""Authentication request and response schemas."""
from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int
    subject: str


class CurrentUserResponse(BaseModel):
    subject: str
    issuer: str
    issued_at: int
    expires_at: int