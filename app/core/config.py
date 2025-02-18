from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # JWT settings
    SECRET_KEY: str = "tu_clave_secreta_aqui_muy_segura_y_larga_2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

    # Database settings
    DB_USER: str = Field(alias="db_user")
    DB_PASSWORD: str = Field(alias="db_password")
    DB_HOST: str = Field(alias="db_host")
    DB_PORT: str = Field(alias="db_port")
    DB_NAME: str = Field(alias="db_name")

    # TMDB settings
    TMDB_API_KEY: str = Field(alias="tmdb_api_key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings() 