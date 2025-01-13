from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.rating import Rating, RatingCreate
from app.services.rating_service import RatingService
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Rating)
async def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    rating_service = RatingService(db)
    created_rating = rating_service.create_rating(rating)
    return created_rating

@router.get("/{rating_id}", response_model=Rating)
async def get_rating(rating_id: int, db: Session = Depends(get_db)):
    rating_service = RatingService(db)
    rating = rating_service.get_rating(rating_id)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@router.get("/", response_model=List[Rating])
async def get_all_ratings(db: Session = Depends(get_db)):
    rating_service = RatingService(db)
    return rating_service.get_all_ratings()

@router.put("/{rating_id}", response_model=Rating)
async def update_rating(rating_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    rating_service = RatingService(db)
    updated_rating = rating_service.update_rating(rating_id, rating)
    if updated_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return updated_rating

@router.delete("/{rating_id}", response_model=bool)
async def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating_service = RatingService(db)
    success = rating_service.delete_rating(rating_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rating not found")
    return success