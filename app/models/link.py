from sqlalchemy import Column, Integer, Float
from app.database import Base

class Link(Base):
    __tablename__ = "links"

    movie_id = Column(Integer, primary_key=True, index=True)
    imdb_id = Column(Integer, nullable=False)
    tmdb_id = Column(Float, nullable=True)