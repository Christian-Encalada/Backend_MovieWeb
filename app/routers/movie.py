from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.movie import Movie, MovieCreate
from app.services.movie_service import MovieService
from app.dependencies import get_db
from app.services.rating_service import RatingService
from app.middlewares.auth import get_current_user
from app.models.user import User
from app.models.movie import Movie as MovieModel
from collections import Counter
import random

router = APIRouter()

@router.post("/", response_model=Movie)
async def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    created_movie = movie_service.create_movie(movie)
    return created_movie

@router.get("/", response_model=List[Movie])
async def get_all_movies(db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    return movie_service.get_all_movies()

@router.get("/search", response_model=List[Movie])
async def search_movies(
    term: str = Query(..., description="Término de búsqueda", min_length=1),
    db: Session = Depends(get_db)
):
    movie_service = MovieService(db)
    movies = movie_service.search_movies_by_title(term)
    return movies

@router.get("/genre/{genre}", response_model=List[Movie])
async def get_movies_by_genre(genre: str, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    return movie_service.get_movies_by_genre(genre)

@router.get("/ratings/movie/{movie_id}")
async def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    rating_service = RatingService(db)
    return rating_service.get_movie_ratings(movie_id)

@router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    movie = movie_service.get_movie_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@router.get("/{movie_id}/similar", response_model=List[Movie])
async def get_similar_movies(movie_id: int, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    similar_movies = movie_service.get_similar_movies(movie_id)
    if not similar_movies:
        raise HTTPException(status_code=404, detail="No similar movies found")
    return similar_movies

@router.put("/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    updated_movie = movie_service.update_movie(movie_id, movie)
    if updated_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie

@router.delete("/{movie_id}", response_model=bool)
async def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie_service = MovieService(db)
    success = movie_service.delete_movie(movie_id)
    if not success:
        raise HTTPException(status_code=404, detail="Movie not found")
    return success

@router.get("/recommendations/user", response_model=List[Movie])
async def get_recommendations_by_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized movie recommendations for the authenticated user.
    
    - **current_user**: Automatically obtained from the JWT token
    - Returns a list of recommended movies based on user's favorites
    """
    try:
        print(f"User ID: {current_user.user_id}")  # Debug log
        print(f"User favs: {current_user.favs}")   # Debug log

        # Si el usuario no tiene favoritos o favs es None
        if not current_user.favs or current_user.favs is None:
            print("No favorites found, returning random movies")  # Debug log
            all_movies = db.query(MovieModel).limit(10).all()
            return [movie.to_dict() for movie in all_movies]

        # Obtener las películas favoritas del usuario
        fav_movies = db.query(MovieModel).filter(MovieModel.movie_id.in_(current_user.favs)).all()
        print(f"Found {len(fav_movies)} favorite movies")  # Debug log
        
        if not fav_movies:
            print("No favorite movies found in database")  # Debug log
            all_movies = db.query(MovieModel).limit(10).all()
            return [movie.to_dict() for movie in all_movies]

        # Obtener películas similares basadas en el primer favorito
        recommended = (
            db.query(MovieModel)
            .filter(MovieModel.movie_id.notin_(current_user.favs))
            .limit(10)
            .all()
        )

        print(f"Found {len(recommended)} recommendations")  # Debug log
        return [movie.to_dict() for movie in recommended]

    except Exception as e:
        print(f"Error in recommendations: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_movies(title: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{title}%")).limit(5).all()
    return movies

@router.get("/top-rated", response_model=List[Movie])
async def get_top_rated_movies(limit: int = 10, db: Session = Depends(get_db)):
    movies = (
        db.query(MovieModel)
        .order_by(MovieModel.rating.desc())
        .limit(limit)
        .all()
    )
    return movies