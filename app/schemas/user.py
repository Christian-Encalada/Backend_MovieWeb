from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str
    favs: Optional[List[int]] = []  # Añadir una lista de IDs de películas favoritas

class User(UserBase):
    user_id: int
    favs: List[int] = []

    class Config:
        from_attributes = True  # Renombrado de orm_mode en Pydantic v2
        arbitrary_types_allowed = True  # Permitir tipos arbitrarios