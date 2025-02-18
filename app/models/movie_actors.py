from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class MovieActor(Base):
    __tablename__ = "movie_actors"

    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.actor_id", ondelete="CASCADE"), primary_key=True) 