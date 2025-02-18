from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
    preferred_genres = relationship(
        "UserPreferredGenres",
        back_populates="user",
        cascade="all, delete-orphan"
    )