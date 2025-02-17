from sqlalchemy import Column, Integer, String, Float, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genres = Column(String)
    tmdb_id = Column(Integer, unique=True)
    poster_path = Column(String)
    overview = Column(Text)
    release_date = Column(Date)
    vote_average = Column(Float)
    vote_count = Column(Integer)
    
    actors = relationship(
        "Actor",
        secondary="movie_actors",
        back_populates="movies",
        primaryjoin="Movie.movie_id==MovieActor.movie_id",
        secondaryjoin="MovieActor.actor_id==Actor.actor_id"
    )

    def to_dict(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "genres": self.genres
        }