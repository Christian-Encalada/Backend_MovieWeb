from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config import settings
from app.models.user import User
from sqlalchemy.orm import Session
from app.dependencies import get_db
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

security = HTTPBearer()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Agregar logs para debug
        print(f"Token recibido: {token[:20]}...")
        
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        print(f"Payload decodificado: {payload}")  # Debug
        
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        # Convertir user_id a int
        try:
            user_id = int(user_id)
        except ValueError:
            print(f"Error convirtiendo user_id: {user_id}")
            raise credentials_exception

        user = db.query(User).filter(User.user_id == user_id).first()
        if user is None:
            print(f"Usuario no encontrado para ID: {user_id}")
            raise credentials_exception

        print(f"Usuario autenticado: {user.user_id} - {user.username}")
        return user
        
    except JWTError as e:
        print(f"Error JWT: {str(e)}")
        raise credentials_exception
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        raise credentials_exception 

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        print(f"Verificando token en middleware: {token[:20]}...")  # Debug
        print(f"Usando SECRET_KEY: {settings.SECRET_KEY[:5]}...")  # Debug

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        print(f"Token verificado exitosamente")  # Debug
        return payload
    except JWTError as e:
        print(f"Error verificando token: {str(e)}")  # Debug
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        ) 