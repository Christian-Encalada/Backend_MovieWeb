from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # JWT settings
    secret_key: str  # Cambiado a minúsculas para coincidir con el .env
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
    ssl_cert: str | None = None  # Hacemos el campo opcional

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=False  # Esto es importante
    )

settings = Settings()