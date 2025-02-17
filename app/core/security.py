from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Configuración
SECRET_KEY = "tu_clave_secreta_muy_segura"  # Cambiar en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    
    try:
        logger.info(f"Creando token con datos: {to_encode}")
        logger.info(f"Usando SECRET_KEY: {settings.secret_key[:5]}...")
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.secret_key,
            algorithm=settings.algorithm
        )
        logger.info(f"Token creado exitosamente: {encoded_jwt[:20]}...")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creando token: {str(e)}")
        raise e 