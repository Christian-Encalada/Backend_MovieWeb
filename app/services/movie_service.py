from sqlalchemy.orm import Session
from app.models.movie import Movie as MovieModel
from app.schemas.movie import MovieCreate, Movie as MovieSchema

class MovieService:
    def __init__(self, db: Session):
        self.db = db

    def create_movie(self, movie: MovieCreate) -> MovieSchema:
        db_movie = MovieModel(movie_id=movie.movie_id, title=movie.title, genres=movie.genres)
        self.db.add(db_movie)
        self.db.commit()
        self.db.refresh(db_movie)
        return db_movie

    def get_movie(self, movie_id: int) -> MovieSchema:
        return self.db.query(MovieModel).filter(MovieModel.movie_id == movie_id).first()

    def get_all_movies(self) -> list[MovieSchema]:
        return self.db.query(MovieModel).all()

    def update_movie(self, movie_id: int, movie: MovieCreate) -> MovieSchema:
        db_movie = self.db.query(MovieModel).filter(MovieModel.movie_id == movie_id).first()
        if db_movie:
            db_movie.title = movie.title
            db_movie.genres = movie.genres
            self.db.commit()
            self.db.refresh(db_movie)
        return db_movie

    def delete_movie(self, movie_id: int) -> bool:
        db_movie = self.db.query(MovieModel).filter(MovieModel.movie_id == movie_id).first()
        if db_movie:
            self.db.delete(db_movie)
            self.db.commit()
            return True
        return False

    def get_movie_by_id(self, movie_id: int):
        return self.db.query(MovieModel).filter(MovieModel.movie_id == movie_id).first()

    def get_movies_by_genre(self, genre: str):
        return self.db.query(MovieModel).filter(MovieModel.genres.contains(genre)).all()

    def search_movies_by_title(self, term: str) -> list[MovieSchema]:
        try:
            return (
                self.db.query(MovieModel)
                .filter(MovieModel.title.ilike(f"%{term}%"))
                .limit(10)
                .all()
            )
        except Exception as e:
            print(f"Error en búsqueda: {str(e)}")
            return []

    def get_similar_movies(self, movie_id: int) -> list[MovieSchema]:
        try:
            # Obtener la película base
            base_movie = self.get_movie_by_id(movie_id)
            if not base_movie:
                return []

            # Obtener los géneros de la película base
            base_genres = set(base_movie.genres.split('|'))

            # Buscar películas con géneros similares
            similar_movies = (
                self.db.query(MovieModel)
                .filter(MovieModel.movie_id != movie_id)  # Excluir la película actual
                .all()
            )

            # Calcular similitud por géneros
            movie_scores = []
            for movie in similar_movies:
                movie_genres = set(movie.genres.split('|'))
                # Calcular intersección de géneros
                common_genres = len(base_genres.intersection(movie_genres))
                if common_genres > 0:
                    movie_scores.append((movie, common_genres))

            # Ordenar por cantidad de géneros en común y tomar los primeros 8
            movie_scores.sort(key=lambda x: x[1], reverse=True)
            return [movie for movie, _ in movie_scores[:8]]

        except Exception as e:
            print(f"Error obteniendo películas similares: {str(e)}")
            return []