"""Application settings using Pydantic v2.
Environment variables override the defaults. These settings are imported
across the application (database, Celery, security, storage)."""
from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # ───────────────────────────── Database
    DATABASE_URL: str = "postgresql+asyncpg://dev:devpass@db:5432/amm"

    # ───────────────────────────── Security
    JWT_SECRET: str = "supersecretchange"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # ───────────────────────────── Redis / Celery
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str | None = None  # fallback to REDIS_URL
    CELERY_RESULT_BACKEND: str | None = None

    # ───────────────────────────── S3 / MinIO
    MINIO_ENDPOINT: str = "http://minio:9000"
    MINIO_ACCESS_KEY: str = "minio"
    MINIO_SECRET_KEY: str = "minio123"
    MINIO_BUCKET: str = "files"

    # ───────────────────────────── Environment
    ENVIRONMENT: Literal["local", "test", "production"] = "local"

    @property
    def broker_url(self) -> str:
        return self.CELERY_BROKER_URL or self.REDIS_URL

    @property
    def result_backend(self) -> str:
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    return Settings()
