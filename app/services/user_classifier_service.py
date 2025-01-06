from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.models.movie import Movie as MovieModel

class UserClassifierService:
    def __init__(self, db: Session):
        self.db = db

    def classify_user_genres(self, user_id: int) -> list[str]:
        user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if not user:
            raise KeyError("User not found")

        genres = [
            "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Family", "Fantasy", "History",
            "Horror", "Music", "Mystery", "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western", "Anime"
        ]

        genre_counts = {genre: 0 for genre in genres}
        for movie_id in user.favs:
            movie = self.db.query(MovieModel).filter(MovieModel.movie_id == movie_id).first()
            if movie:
                movie_genres = movie.genres.split('|')
                for genre in movie_genres:
                    if genre in genre_counts:
                        genre_counts[genre] += 1

        sorted_genres = sorted(genre_counts.items(), key=lambda item: item[1], reverse=True)
        top_genres = [genre for genre, count in sorted_genres[:5]]

        return top_genres