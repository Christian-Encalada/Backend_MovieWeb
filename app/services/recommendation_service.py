from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.models.favorite import Favorite
from app.models.actor import Actor
from app.models.movie_actors import MovieActor
from collections import Counter
from app.services.tmdb_service import TMDBService

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.tmdb_service = TMDBService()

    async def get_recommendations_for_user(self, user_id: int) -> list[dict]:
        try:
            # Obtener favoritos del usuario
            favorites = self.db.query(Favorite).filter(Favorite.user_id == user_id).all()
            
            if not favorites:
                return {
                    "message": "No tienes preferencias aún. Agrega películas a favoritos para obtener recomendaciones personalizadas.",
                    "movies": []
                }

            # Obtener géneros de las películas favoritas
            favorite_genres = set()
            favorite_actors = set()

            for fav in favorites:
                # Obtener detalles de la película de TMDB
                movie_details = await self.tmdb_service.get_movie_details(fav.movie_id)
                
                # Agregar géneros
                for genre in movie_details.get('genres', []):
                    favorite_genres.add(genre['id'])
                
                # Agregar actores principales
                credits = await self.tmdb_service.get_movie_credits(fav.movie_id)
                for cast in credits.get('cast', [])[:3]:  # Top 3 actores
                    favorite_actors.add(cast['id'])

            # Obtener recomendaciones basadas en géneros y actores
            recommendations = []
            
            # Obtener películas por géneros similares
            for genre_id in favorite_genres:
                genre_movies = await self.tmdb_service.discover_movies_by_genre(genre_id)
                recommendations.extend(genre_movies)

            # Obtener películas por actores
            for actor_id in favorite_actors:
                actor_movies = await self.tmdb_service.discover_movies_by_actor(actor_id)
                recommendations.extend(actor_movies)

            # Filtrar películas que ya están en favoritos
            favorite_ids = {fav.movie_id for fav in favorites}
            recommendations = [
                movie for movie in recommendations 
                if movie['id'] not in favorite_ids
            ]

            # Ordenar por popularidad y eliminar duplicados
            seen_movies = set()
            unique_recommendations = []
            for movie in sorted(recommendations, key=lambda x: x['vote_average'], reverse=True):
                if movie['id'] not in seen_movies:
                    seen_movies.add(movie['id'])
                    unique_recommendations.append({
                        "movie_id": movie['id'],
                        "title": movie['title'],
                        "genres": "|".join(
                            self.tmdb_service.genres_map.get(genre_id, "Unknown")
                            for genre_id in movie.get('genre_ids', [])
                        ),
                        "poster_path": movie.get('poster_path'),
                        "overview": movie.get('overview'),
                        "release_date": movie.get('release_date'),
                        "vote_average": movie.get('vote_average')
                    })

            return {
                "message": "Recomendaciones basadas en tus favoritos",
                "movies": unique_recommendations[:10]  # Retornar top 10
            }

        except Exception as e:
            print(f"Error getting recommendations: {str(e)}")
            raise