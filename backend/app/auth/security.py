"""JWT helpers implemented without external dependencies."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


@dataclass(frozen=True)
class TokenClaims:
    """Minimal JWT claims used by the app."""

    subject: str
    issued_at: int
    expires_at: int
    issuer: str = "talentmind-ai"

    def to_dict(self) -> dict[str, Any]:
        return {
            "sub": self.subject,
            "iat": self.issued_at,
            "exp": self.expires_at,
            "iss": self.issuer,
        }


def create_access_token(subject: str, secret: str, expires_in_minutes: int, issuer: str = "talentmind-ai") -> str:
    """Create a signed HS256 JWT."""

    now = datetime.now(timezone.utc)
    claims = TokenClaims(
        subject=subject,
        issued_at=int(now.timestamp()),
        expires_at=int((now + timedelta(minutes=expires_in_minutes)).timestamp()),
        issuer=issuer,
    )
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = _b64encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    encoded_payload = _b64encode(json.dumps(claims.to_dict(), separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    encoded_signature = _b64encode(signature)
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def verify_access_token(token: str, secret: str, issuer: str = "talentmind-ai") -> dict[str, Any]:
    """Verify an HS256 JWT and return its claims."""

    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise ValueError("Invalid token format") from exc

    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    expected_signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(_b64encode(expected_signature), encoded_signature):
        raise ValueError("Invalid token signature")

    header = json.loads(_b64decode(encoded_header))
    if header.get("alg") != "HS256":
        raise ValueError("Unsupported token algorithm")

    claims = json.loads(_b64decode(encoded_payload))
    if claims.get("iss") != issuer:
        raise ValueError("Invalid token issuer")

    expires_at = int(claims.get("exp", 0))
    if expires_at <= int(datetime.now(timezone.utc).timestamp()):
        raise ValueError("Token has expired")

    return claims