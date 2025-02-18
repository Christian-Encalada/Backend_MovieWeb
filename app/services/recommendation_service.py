from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.models.favorite import Favorite
from app.models.actor import Actor
from app.models.movie_actors import MovieActor
from collections import Counter
from app.services.tmdb_service import TMDBService
from typing import Dict
from fastapi import HTTPException

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.tmdb_service = TMDBService()

    async def get_recommendations_for_user(self, user_id: int) -> Dict:
        try:
            # Obtener favoritos del usuario
            favorites = (
                self.db.query(Favorite)
                .filter(Favorite.user_id == user_id)
                .all()
            )

            if not favorites:
                return {"movies": []}

            # Obtener recomendaciones basadas en los favoritos
            all_recommendations = []
            for favorite in favorites[:5]:  # Usar solo los últimos 5 favoritos
                try:
                    recommendations = await self.tmdb_service.get_movie_recommendations(favorite.movie_id)
                    all_recommendations.extend(recommendations)
                except Exception as e:
                    print(f"Error getting recommendations for movie {favorite.movie_id}: {str(e)}")
                    continue

            # Eliminar duplicados y convertir al formato de nuestra API
            seen_movies = set()
            unique_recommendations = []
            
            for movie in all_recommendations:
                if movie["id"] not in seen_movies:
                    seen_movies.add(movie["id"])
                    unique_recommendations.append({
                        "movie_id": movie["id"],
                        "title": movie["title"],
                        "genres": "|".join(
                            self.tmdb_service.genres_map.get(genre_id, "Unknown")
                            for genre_id in movie.get("genre_ids", [])
                        ),
                        "poster_path": movie.get("poster_path"),
                        "overview": movie.get("overview"),
                        "release_date": movie.get("release_date"),
                        "vote_average": movie.get("vote_average", 0)
                    })

            return {
                "movies": unique_recommendations[:10]  # Devolver solo las 10 mejores recomendaciones
            }

        except Exception as e:
            print(f"Error in get_recommendations_for_user: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error getting recommendations: {str(e)}"
            )