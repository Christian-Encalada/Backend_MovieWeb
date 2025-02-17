from pydantic import BaseModel, EmailStr, constr, Field, validator
from typing import List, Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None

    @validator('username')
    def validate_username(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre de usuario no puede estar vacío')
        return v.strip() if v else None

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

    model_config = {
        "json_schema_extra": {
            "example": {
                "current_password": "contraseña_actual",
                "new_password": "nueva_contraseña",
                "confirm_password": "nueva_contraseña"
            }
        }
    }