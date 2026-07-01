"""Application settings.

Minimal Pydantic Settings for dev; production should use a secrets manager.
"""
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TalentMind AI"
    debug: bool = Field(default=True)
    database_url: str = Field(default="sqlite:///./dev.db")
    jwt_secret: SecretStr = Field(default=SecretStr("changeme"), validation_alias="JWT_SECRET")
    auth_username: str = Field(default="admin", validation_alias="AUTH_USERNAME")
    auth_password: SecretStr = Field(default=SecretStr("admin"), validation_alias="AUTH_PASSWORD")
    require_auth: bool = Field(default=False, validation_alias="REQUIRE_AUTH")
    access_token_expiry_minutes: int = Field(default=60, ge=1, le=24 * 60)
    rate_limit_requests_per_minute: int = Field(default=120, ge=1)
    rate_limit_window_seconds: int = Field(default=60, ge=1)
    vector_store_type: str = Field(default="faiss")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
