from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import User, UserCreate
from app.services.user_service import UserService
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    created_user = user_service.create_user(user)
    return created_user

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