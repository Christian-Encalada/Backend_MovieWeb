from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # JWT settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 horas
    
    # Database settings
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    # TMDB settings
    tmdb_api_key: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"

    # SSL settings
    ssl_cert: Optional[str] = None

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()