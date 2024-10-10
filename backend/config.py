from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, extra="ignore"):
    # Postgres DB
    POSTGRES_CONN_STRING: str
    POSTGRES_HOSTNAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URI: str | None = None

    SQL_ALCHEMY_ECHO_SQL: bool = True

    # OpenAI Keys
    OPENAI_KEY: str
    OPENAI_ASSISTANT_ID: str
    OPENAI_VECTOR_STORE_ID: str

    # Authentication
    JWT_ACCESS_TOKEN_EXPIRATION_SECONDS: int = 60 * 60 * 3  # 3 hours
    JWT_REFRESH_TOKEN_EXPIRATION_SECONDS: int = 60 * 60 * 24 * 1  # 1 day
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET_KEY: str

    # Fast API config
    APP_TITLE: str = "QA & Summarization Interface"
    APP_VERSION: str = "0.1"

    model_config = SettingsConfigDict(env_file=".env")

    @model_validator(mode="after")
    def validator(cls, values: "Settings") -> "Settings":
        values.POSTGRES_URI = f"postgresql+asyncpg://{values.POSTGRES_USER}:{values.POSTGRES_PASSWORD}@{values.POSTGRES_HOSTNAME}:{values.POSTGRES_PORT}/{values.POSTGRES_DB}"
        return values


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
