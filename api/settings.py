from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_dsn: str
    jwt_secret: str
    is_local: bool = False

    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / '.env'),
        env_file_encoding='utf-8',
    )


settings = Settings()
