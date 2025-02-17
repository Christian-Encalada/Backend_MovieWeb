from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Settings(BaseSettings):
    SECRET_KEY: str = "tu_clave_secreta_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
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

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()