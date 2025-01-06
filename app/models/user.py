from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    favs = Column(ARRAY(Integer))  # Añadir una columna para almacenar IDs de películas favoritas