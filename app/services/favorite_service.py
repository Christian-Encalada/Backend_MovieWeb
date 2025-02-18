from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate
from app.services.tmdb_service import TMDBService

class FavoriteService:
    def __init__(self, db: Session):
        self.db = db
        self.tmdb_service = TMDBService()

    def get_user_favorites(self, user_id: int, skip: int = 0, limit: int = 10):
        return self.db.query(Favorite)\
            .filter(Favorite.user_id == user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_favorites_count(self, user_id: int) -> int:
        return self.db.query(Favorite)\
            .filter(Favorite.user_id == user_id)\
            .count()

    def get_favorite(self, user_id: int, movie_id: int) -> Favorite:
        return self.db.query(Favorite)\
            .filter(Favorite.user_id == user_id, Favorite.movie_id == movie_id)\
            .first()

    def add_favorite(self, user_id: int, favorite: FavoriteCreate) -> Favorite:
        db_favorite = Favorite(
            user_id=user_id,
            movie_id=favorite.movie_id
        )
        self.db.add(db_favorite)
        self.db.commit()
        self.db.refresh(db_favorite)
        return db_favorite

    def remove_favorite(self, user_id: int, movie_id: int) -> bool:
        favorite = self.get_favorite(user_id, movie_id)
        if favorite:
            self.db.delete(favorite)
            self.db.commit()
            return True
        return False

    def clear_favorites(self, user_id: int):
        self.db.query(Favorite)\
            .filter(Favorite.user_id == user_id)\
            .delete()
        self.db.commit()

    def is_favorite(self, user_id: int, movie_id: int) -> bool:
        return self.get_favorite(user_id, movie_id) is not None

    async def get_favorite_movies_details(self, user_id: int, skip: int = 0, limit: int = 10):
        favorites = self.get_user_favorites(user_id, skip, limit)
        movies = []
        for favorite in favorites:
            movie_details = await self.tmdb_service.get_movie_details(favorite.movie_id)
            if movie_details:
                movies.append({
                    "movie_id": movie_details["id"],
                    "title": movie_details["title"],
                    "genres": "|".join(genre["name"] for genre in movie_details.get("genres", [])),
                    "poster_path": movie_details.get("poster_path"),
                    "overview": movie_details.get("overview"),
                    "release_date": movie_details.get("release_date"),
                    "vote_average": movie_details.get("vote_average")
                })
        return movies 