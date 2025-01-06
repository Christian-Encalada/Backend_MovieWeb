from pydantic import BaseModel
from typing import List

class RecommendationResponse(BaseModel):
    movie_id: int
    recommendations: List[str]