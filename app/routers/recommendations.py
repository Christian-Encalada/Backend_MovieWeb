from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.services.recommendation_service import RecommendationService
from app.schemas.movie import Movie
from typing import List
from app.models.user import User

router = APIRouter()

@router.get("/user", response_model=List[Movie])
async def get_personalized_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        recommendation_service = RecommendationService(db)
        recommendations = recommendation_service.get_recommendations_for_user(current_user.user_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}", response_model=List[Movie])
async def get_similar_movies(
    movie_id: int,
    db: Session = Depends(get_db)
):
    recommendation_service = RecommendationService(db)
    return recommendation_service.get_similar_movies(movie_id)