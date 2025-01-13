from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    favs: Optional[List[int]] = []

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    user_id: int
    favs: Optional[List[int]] = []
    created_at: datetime

    class Config:
        from_attributes = True