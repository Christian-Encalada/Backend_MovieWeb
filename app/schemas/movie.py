from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    genres: str | None = None
    poster_path: str | None = None
    overview: str | None = None
    release_date: str | None = None
    vote_average: float | None = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    movie_id: int

    class Config:
        from_attributes = True