from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres DB
    POSTGRES_CONN_STRING: str
    POSTGRES_HOSTNAME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URI: str | None = None

    # OpenAI Keys
    OPENAI_KEY: str
    OPENAI_ASSISTANT_ID: str
    OPENAI_VECTOR_STORE_ID: str

    # Authentication
    JWT_TOKEN_EXPIRATION_DURATION: 60 * 60 * 3 # 3 hours
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

    @model_validator
    def validator(cls, values: "Settings") -> "Settings":
        values.POSTGRES_URI = f"{values.POSTGRES_USER}:{values.POSTGRES_PASSWORD}@{values.POSTGRES_HOSTNAME}:{values.POSTGRES_PORT}/{values.POSTGRES_DB}"
        return values


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
