"""Settings read from the environment. Defaults are for local development only."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    secret_key: str = "dev-only-change-me"
    database_url: str = "sqlite:///./data/rheinclean.db"
    cors_origins: str = "http://127.0.0.1:5173,http://localhost:5173"
    cookie_secure: bool = False
    session_seconds: int = 60 * 60
    environment: str = "development"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
