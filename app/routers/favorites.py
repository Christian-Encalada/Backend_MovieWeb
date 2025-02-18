from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.movie import Movie
from app.services.tmdb_service import TMDBService

router = APIRouter()

@router.get("/", response_model=List[Movie])
async def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        tmdb_service = TMDBService()
        favorites = []
        for movie_id in current_user.favs:
            movie_details = await tmdb_service.get_movie_details(movie_id)
            favorites.append({
                "movie_id": movie_details["id"],
                "title": movie_details["title"],
                "genres": "|".join(genre["name"] for genre in movie_details.get("genres", [])),
                "poster_path": movie_details.get("poster_path"),
                "overview": movie_details.get("overview"),
                "release_date": movie_details.get("release_date"),
                "vote_average": movie_details.get("vote_average")
            })
        return favorites
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{movie_id}")
async def add_to_favorites(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if movie_id not in current_user.favs:
        current_user.favs.append(movie_id)
        db.commit()
    return {"status": "success"}

@router.delete("/{movie_id}")
async def remove_from_favorites(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if movie_id in current_user.favs:
        current_user.favs.remove(movie_id)
        db.commit()
    return {"status": "success"}

@router.get("/{movie_id}/check")
async def check_favorite(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {"isFavorite": movie_id in current_user.favs} 