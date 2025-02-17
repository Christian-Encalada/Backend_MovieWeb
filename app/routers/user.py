from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from typing import List, Dict
from app.schemas.user import User, UserCreate, UserLogin, Token
from app.services.user_service import UserService
from app.dependencies import get_db, get_current_user
from app.models.user import User as UserModel
from app.utils.auth import get_password_hash
from pydantic import BaseModel, validator, Field
from app.core.security import verify_password
from pydantic import EmailStr

router = APIRouter()

# Solo un modelo para actualización de contraseña
class PasswordUpdateSchema(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=1)

    class Config:
        schema_extra = {
            "example": {
                "current_password": "password123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        }

class UserRegisterWithGenres(BaseModel):
    username: str
    email: EmailStr
    password: str
    preferred_genres: List[str]

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    auth_result = user_service.authenticate_user(user.username, user.password)
    
    if not auth_result:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_result

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=List[User])
async def get_all_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    updated_user = user_service.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

@router.post("/favorites/{movie_id}")
async def add_to_favorites(
    movie_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if not current_user.favs:
            current_user.favs = []
        
        if movie_id not in current_user.favs:
            current_user.favs.append(movie_id)
            db.commit()
        
        return {"user_id": current_user.user_id, "favs": current_user.favs}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/favorites/{movie_id}")
async def remove_from_favorites(
    movie_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if current_user.favs and movie_id in current_user.favs:
            current_user.favs.remove(movie_id)
            db.commit()
        
        return {"user_id": current_user.user_id, "favs": current_user.favs}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/password")
async def update_password(
    data: PasswordUpdateSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Verificar contraseña actual
        if not verify_password(data.current_password, current_user.password):
            raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")

        # Verificar que las nuevas contraseñas coincidan
        if data.new_password != data.confirm_password:
            raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

        # Actualizar contraseña
        current_user.password = get_password_hash(data.new_password)
        db.commit()

        return {"message": "Contraseña actualizada exitosamente"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/register-with-genres", response_model=User)
async def register_user_with_genres(
    user_data: UserRegisterWithGenres,
    db: Session = Depends(get_db)
):
    # Verificar usuario existente
    if db.query(UserModel).filter(UserModel.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear usuario
    hashed_password = get_password_hash(user_data.password)
    db_user = UserModel(
        email=user_data.email,
        username=user_data.username,
        password=hashed_password,
        favs=[]
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Agregar géneros preferidos
    for genre in user_data.preferred_genres:
        genre_pref = UserPreferredGenres(
            user_id=db_user.user_id,
            genre=genre
        )
        db.add(genre_pref)
    
    db.commit()
    return db_user