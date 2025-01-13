from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM
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
        print(f"Received token: {token[:20]}...")  # Debug log
        
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            print("No user_id in token")  # Debug log
            raise credentials_exception

        print(f"Token decoded, user_id: {user_id}")  # Debug log

        # Obtener el usuario
        user = db.query(User).filter(User.user_id == int(user_id)).first()
        
        if user is None:
            print(f"No user found for id {user_id}")  # Debug log
            raise credentials_exception

        # Asegurarse de que favs sea una lista
        if user.favs is None:
            user.favs = []
            db.commit()

        print(f"User authenticated: {user.user_id}, favs: {user.favs}")  # Debug log
        return user

    except JWTError as e:
        print(f"JWT Error: {str(e)}")  # Debug log
        raise credentials_exception
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        raise credentials_exception 