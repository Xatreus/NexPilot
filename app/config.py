"""Environment-backed settings."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "NexPilot"
    environment: str = "development"
    database_url: str = "sqlite:///./data/nexpilot.db"
    github_token: str | None = None
    openrouter_api_key: str | None = None
    openrouter_model: str = "deepseek/deepseek-chat-v3-0324:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    request_timeout_seconds: float = 12.0
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
