from typing import Optional
from pydantic import BaseModel

class RatingBase(BaseModel):
    movie_id: int
    rating: float

class RatingCreate(RatingBase):
    user_id: Optional[int] = None

class Rating(RatingBase):
    rating_id: int
    user_id: Optional[int]

    class Config:
        from_attributes = True