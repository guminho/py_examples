from pydantic import Field, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str = "MyService"

    DEBUG: bool = False

    # Pydantic validates that these are actually valid URLs
    DATABASE_URL: PostgresDsn
    CACHE_URL: RedisDsn = Field(default="redis://localhost:6379/0")

    # SecretStr prevents the value from being leaked in logs/print statements
    API_KEY: SecretStr
    JWT_SECRET: SecretStr

    # 4. Config Loading Logic
    model_config = SettingsConfigDict(
        # Looks for .env file, but System Env Vars always win (12-Factor rule)
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Instantiate once to be used as a singleton across the app
cfg = AppSettings()
