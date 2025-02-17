from fastapi import APIRouter, HTTPException, Depends, status, Body
from sqlalchemy.orm import Session
from typing import List, Dict
from app.schemas.user import User, UserCreate, UserLogin
from app.services.user_service import UserService
from app.dependencies import get_db, get_current_user
from app.models.user import User as UserModel
from app.utils.auth import get_password_hash
from pydantic import BaseModel, validator, Field
from app.core.security import verify_password

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
        favs=user.favs
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    auth_result = user_service.authenticate_user(user.username, user.password)
    
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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

@router.get("/favorites", response_model=dict)
async def get_favorites(current_user: UserModel = Depends(get_current_user)):
    try:
        # Asegurarnos de que favs sea una lista
        user_favs = current_user.favs if isinstance(current_user.favs, list) else []
        return {
            "user_id": current_user.user_id,
            "favs": user_favs
        }
    except Exception as e:
        print(f"Error getting favorites: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting favorites"
        )

@router.post("/favorites")
async def add_to_favorites(
    data: Dict[str, int] = Body(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    movie_id = data.get("movie_id")
    if not movie_id:
        raise HTTPException(status_code=400, detail="movie_id is required")
    
    user_service = UserService(db)
    updated_user = user_service.add_to_favorites(current_user.user_id, movie_id)
    return {"user_id": updated_user.user_id, "favs": updated_user.favs or []}

@router.delete("/favorites/{movie_id}")
async def remove_from_favorites(
    movie_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    updated_user = user_service.remove_from_favorites(current_user.user_id, movie_id)
    return {"user_id": updated_user.user_id, "favs": updated_user.favs}

@router.put("/password")
async def update_password(
    password_data: PasswordUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    print(f"Actualizando contraseña para usuario {current_user.user_id}")
    print(f"Datos recibidos: {password_data.dict()}")

    try:
        # Verificar contraseña actual
        if not verify_password(password_data.current_password, current_user.password):
            raise HTTPException(
                status_code=400,
                detail="La contraseña actual es incorrecta"
            )

        # Verificar que las contraseñas coincidan
        if password_data.new_password != password_data.confirm_password:
            raise HTTPException(
                status_code=400,
                detail="Las contraseñas nuevas no coinciden"
            )

        # Actualizar contraseña
        current_user.password = get_password_hash(password_data.new_password)
        db.commit()

        return {"message": "Contraseña actualizada exitosamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )