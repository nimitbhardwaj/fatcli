from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FATSECRET_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    consumer_key: str = ""
    consumer_secret: str = ""
    config_dir: Path = Path.home() / ".config" / "fatsecret"


settings = Settings()
