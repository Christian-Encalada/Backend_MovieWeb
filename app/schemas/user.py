from pydantic import BaseModel, EmailStr, constr, Field, validator
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

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('La nueva contraseña debe tener al menos 8 caracteres')
        return v

    @validator('confirm_password')
    def validate_passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Las contraseñas no coinciden')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "current_password": "contraseña_actual",
                "new_password": "nueva_contraseña",
                "confirm_password": "nueva_contraseña"
            }
        }