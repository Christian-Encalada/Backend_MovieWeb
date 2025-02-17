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
from app.services.tmdb_service import TMDBService
import requests
from app.services.recommendation_service import RecommendationService

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
    term: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    try:
        tmdb_service = TMDBService()
        movies = await tmdb_service.search_movies(term)
        
        # Agregar log para debug
        print(f"TMDB search results: {movies[:2]}")  # Solo mostramos los primeros 2 resultados
        
        # Convertir resultados de TMDB al formato de nuestra API
        return [
            {
                "movie_id": movie["id"],
                "title": movie["title"],
                "genres": "|".join(
                    tmdb_service.genres_map.get(genre_id, "Unknown")
                    for genre_id in movie.get("genre_ids", [])
                ),
                "poster_path": movie.get("poster_path"),
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average")
            }
            for movie in movies
        ]
    except Exception as e:
        print(f"Error in search_movies: {str(e)}")  # Log del error
        raise HTTPException(
            status_code=500,
            detail=f"Error searching movies: {str(e)}"
        )

@router.get("/genre/{genre}", response_model=List[Movie])
async def get_movies_by_genre(
    genre: str, 
    db: Session = Depends(get_db)
):
    try:
        tmdb_service = TMDBService()
        # Encontrar el ID del género
        genre_id = None
        for id, name in tmdb_service.genres_map.items():
            if name.lower() == genre.lower():
                genre_id = id
                break
        
        if not genre_id:
            raise HTTPException(status_code=404, detail="Genre not found")
        
        # Obtener películas por género
        url = f"{tmdb_service.base_url}/discover/movie"
        params = {
            "api_key": tmdb_service.api_key,
            "language": "es-ES",
            "with_genres": genre_id,
            "sort_by": "popularity.desc"
        }
        response = requests.get(url, params=params)
        movies = response.json()["results"]
        
        return [
            {
                "movie_id": movie["id"],
                "title": movie["title"],
                "genres": "|".join(
                    tmdb_service.genres_map.get(genre_id, "Unknown")
                    for genre_id in movie.get("genre_ids", [])
                ),
                "poster_path": movie.get("poster_path"),
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average")
            }
            for movie in movies
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    try:
        tmdb_service = TMDBService()
        movies = await tmdb_service.get_movie_recommendations(movie_id)
        
        return [
            {
                "movie_id": movie["id"],
                "title": movie["title"],
                "genres": "|".join(
                    tmdb_service.genres_map.get(genre_id, "Unknown")
                    for genre_id in movie.get("genre_ids", [])
                ),
                "poster_path": movie.get("poster_path"),
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average")
            }
            for movie in movies
        ]
    except Exception as e:
        print(f"Error getting recommendations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting movie recommendations: {str(e)}"
        )

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
    try:
        print("Usuario recibido en recomendaciones:", current_user.user_id)
        
        recommendation_service = RecommendationService(db)
        recommendations = await recommendation_service.get_recommendations_for_user(current_user.user_id)
        
        print("Recomendaciones obtenidas:", len(recommendations['movies']))
        
        if not recommendations['movies']:
            print("No se encontraron recomendaciones")
            return []
        
        return recommendations['movies']

    except Exception as e:
        print("Error en recomendaciones:", str(e))
        print("Tipo de error:", type(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/top-rated", response_model=List[Movie])
async def get_top_rated_movies(limit: int = 10, db: Session = Depends(get_db)):
    movies = (
        db.query(MovieModel)
        .order_by(MovieModel.rating.desc())
        .limit(limit)
        .all()
    )
    return movies