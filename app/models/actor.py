from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    tmdb_id = Column(Integer, unique=True)
    
    movies = relationship("Movie", secondary="movie_actors", back_populates="actors") 