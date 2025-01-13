from sqlalchemy.orm import Session
from app.models.movie import Movie as MovieModel
from app.models.user import User as UserModel
from collections import Counter
from typing import List
import random

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def get_recommendations_for_user(self, user_id: int) -> List[MovieModel]:
        try:
            # Obtener el usuario y sus favoritos
            user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
            if not user or not user.favs:
                # Si el usuario no tiene favoritos, devolver películas aleatorias
                all_movies = self.db.query(MovieModel).all()
                return random.sample(all_movies, min(10, len(all_movies)))

            # Obtener las películas favoritas del usuario
            fav_movies = self.db.query(MovieModel).filter(MovieModel.movie_id.in_(user.favs)).all()
            
            # Recolectar todos los géneros de las películas favoritas
            genre_counter = Counter()
            for movie in fav_movies:
                genres = movie.genres.split('|')
                genre_counter.update(genres)

            # Obtener los 3 géneros más frecuentes
            top_genres = [genre for genre, _ in genre_counter.most_common(3)]
            
            if not top_genres:
                return []

            # Buscar películas similares basadas en los géneros preferidos
            # que no estén en los favoritos del usuario
            recommended_movies = (
                self.db.query(MovieModel)
                .filter(
                    MovieModel.movie_id.notin_(user.favs),  # Excluir favoritos
                    MovieModel.genres.contains(top_genres[0])  # Debe contener al menos el género más común
                )
                .order_by(MovieModel.movie_id)  # Ordenar para consistencia
                .limit(10)
                .all()
            )

            return recommended_movies

        except Exception as e:
            print(f"Error getting recommendations: {str(e)}")
            return []