from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str
    genres: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    movie_id: int

    class Config:
        from_attributes = True