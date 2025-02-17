from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.database import SessionLocal
from app.models.user import User
from app.config import settings
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        logger.info(f"Recibido token: {token[:10]}...")
        logger.info(f"SECRET_KEY: {settings.secret_key[:5]}...")
        
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        
        logger.info(f"Payload decodificado: {payload}")
        
        user_id = payload.get("sub")
        if user_id is None:
            logger.error("No se encontró sub en el payload")
            raise credentials_exception
            
        user_id = int(user_id)
        
        user = db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            logger.error(f"No se encontró usuario con ID {user_id}")
            raise credentials_exception
            
        logger.info(f"Usuario autenticado: {user.username}")
        return user
        
    except JWTError as e:
        logger.error(f"Error JWT: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise credentials_exception