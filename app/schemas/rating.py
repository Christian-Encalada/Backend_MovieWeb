from pydantic import BaseModel

class RatingBase(BaseModel):
    movie_id: int
    rating: float

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # Renombrado de orm_mode en Pydantic v2
        arbitrary_types_allowed = True  # Permitir tipos arbitrarios