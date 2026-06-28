"""Application settings.

Minimal Pydantic Settings for dev; production should use a secrets manager.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "TalentMind AI"
    debug: bool = Field(default=True)
    database_url: str = Field(default="sqlite:///./dev.db")
    jwt_secret: str = Field(default="changeme", env="JWT_SECRET")
    vector_store_type: str = Field(default="faiss")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
