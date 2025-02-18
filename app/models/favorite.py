from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(Integer, nullable=False)  # ID de TMDB
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con el usuario
    user = relationship("User", back_populates="favorites") 