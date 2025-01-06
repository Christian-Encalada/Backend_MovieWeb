from sqlalchemy import Column, Integer, String
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(String, nullable=False)  # Lista de géneros separados por '|'