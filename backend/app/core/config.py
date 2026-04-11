from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_env: str = "development"
    app_name: str = "llm-profiler"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Security
    secret_key: str
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore", 
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Use as a FastAPI dependency: settings = Depends(get_settings)
    """
    return Settings()