from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.schemas.favorite import FavoriteCreate, Favorite
from app.schemas.movie import Movie
from app.services.favorite_service import FavoriteService
from app.models.user import User
from app.models.favorite import Favorite as FavoriteModel

router = APIRouter()

# CREATE
@router.post("/{movie_id}")
async def add_to_favorites(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Verificar si ya existe en favoritos
        existing_favorite = db.query(FavoriteModel).filter(
            FavoriteModel.user_id == current_user.user_id,
            FavoriteModel.movie_id == movie_id
        ).first()

        if existing_favorite:
            raise HTTPException(
                status_code=400,
                detail="Movie already in favorites"
            )

        # Crear nuevo favorito
        new_favorite = FavoriteModel(
            user_id=current_user.user_id,
            movie_id=movie_id
        )
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)

        return {"status": "success", "message": "Movie added to favorites"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# READ
@router.get("/", response_model=List[Movie])
async def get_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Obtener lista de películas favoritas con paginación"""
    favorite_service = FavoriteService(db)
    return await favorite_service.get_favorite_movies_details(current_user.user_id, skip, limit)

@router.get("/count")
async def get_favorites_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener cantidad total de favoritos"""
    favorite_service = FavoriteService(db)
    return {"count": favorite_service.get_favorites_count(current_user.user_id)}

@router.get("/check/{movie_id}")
async def check_favorite(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorite = db.query(FavoriteModel).filter(
        FavoriteModel.user_id == current_user.user_id,
        FavoriteModel.movie_id == movie_id
    ).first()

    return {"isFavorite": favorite is not None}

@router.get("/{movie_id}", response_model=Favorite)
async def get_favorite(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener detalle de un favorito específico"""
    favorite_service = FavoriteService(db)
    favorite = favorite_service.get_favorite(current_user.user_id, movie_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return favorite

# DELETE
@router.delete("/{movie_id}")
async def remove_from_favorites(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        favorite = db.query(FavoriteModel).filter(
            FavoriteModel.user_id == current_user.user_id,
            FavoriteModel.movie_id == movie_id
        ).first()

        if not favorite:
            raise HTTPException(
                status_code=404,
                detail="Movie not found in favorites"
            )

        db.delete(favorite)
        db.commit()

        return {"status": "success", "message": "Movie removed from favorites"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
async def clear_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar todos los favoritos del usuario"""
    favorite_service = FavoriteService(db)
    favorite_service.clear_favorites(current_user.user_id)
    return {"status": "success"} 