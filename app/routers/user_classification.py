from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.user_classification_response import UserClassificationResponse
from app.services.user_classifier_service import UserClassifierService
from app.dependencies import get_db

router = APIRouter()

@router.get("/{user_id}", response_model=UserClassificationResponse)
async def classify_user(user_id: int, db: Session = Depends(get_db)):
    user_classifier_service = UserClassifierService(db)
    try:
        genres = user_classifier_service.classify_user_genres(user_id)
        return UserClassificationResponse(user_id=user_id, classification=genres)
    except KeyError:
        raise HTTPException(status_code=404, detail="User not found")