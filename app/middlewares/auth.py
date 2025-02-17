from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings  # Importar settings
from app.services.user_service import UserService
from app.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        print("Token recibido:", token[:20], "...")  # Log del token
        
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        print("Payload decodificado:", payload)  # Log del payload
        
        user_id: str = payload.get("sub")
        if user_id is None:
            print("No se encontró user_id en el payload")
            raise credentials_exception

        user = db.query(User).filter(User.user_id == int(user_id)).first()
        if user is None:
            print(f"No se encontró usuario con ID {user_id}")
            raise credentials_exception

        print("Usuario autenticado:", user.user_id, user.username)  # Log del usuario
        return user

    except JWTError as e:
        print("Error JWT:", str(e))
        raise credentials_exception
    except Exception as e:
        print("Error inesperado:", str(e))
        raise credentials_exception 