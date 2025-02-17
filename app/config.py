from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # JWT settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # Database settings
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    ssl_cert: str

    # TMDB settings
    tmdb_api_key: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(f"Cargada SECRET_KEY: {self.secret_key[:5]}...")
        logger.info(f"Algoritmo configurado: {self.algorithm}")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

settings = Settings()