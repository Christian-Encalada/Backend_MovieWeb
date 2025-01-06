from fastapi import APIRouter, HTTPException
from app.schemas.recommendation_response import RecommendationResponse
from app.services.recommendation_service import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()

@router.get("/{movie_id}", response_model=RecommendationResponse)
async def get_recommendation(movie_id: int):
    try:
        recommendations = recommendation_service.get_recommendations(movie_id)
        recommendations = [str(rec) for rec in recommendations]
        return RecommendationResponse(movie_id=movie_id, recommendations=recommendations)
    except KeyError:
        raise HTTPException(status_code=404, detail="Movie not found")