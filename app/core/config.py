from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    ai_base_url: Optional[str] = None
    upload_dir: str = "/tmp/uploads"
    ai_provider: str = "openai"
    jwt_secret: str = "SUPER_SECRET_KEY_CHANGE_ME"
    database_url: str = "sqlite+aiosqlite:///./db.sqlite"

settings = Settings()
