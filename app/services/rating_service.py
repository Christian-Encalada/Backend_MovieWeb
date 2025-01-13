from sqlalchemy.orm import Session
from app.models.rating import Rating as RatingModel
from app.schemas.rating import RatingCreate, Rating as RatingSchema

class RatingService:
    def __init__(self, db: Session):
        self.db = db

    def create_rating(self, rating: RatingCreate) -> RatingSchema:
        db_rating = RatingModel(user_id=rating.user_id, movie_id=rating.movie_id, rating=rating.rating)
        self.db.add(db_rating)
        self.db.commit()
        self.db.refresh(db_rating)
        return db_rating

    def get_rating(self, rating_id: int) -> RatingSchema:
        return self.db.query(RatingModel).filter(RatingModel.rating_id == rating_id).first()

    def get_all_ratings(self) -> list[RatingSchema]:
        return self.db.query(RatingModel).all()

    def update_rating(self, rating_id: int, rating: RatingCreate) -> RatingSchema:
        db_rating = self.db.query(RatingModel).filter(RatingModel.rating_id == rating_id).first()
        if db_rating:
            db_rating.user_id = rating.user_id
            db_rating.movie_id = rating.movie_id
            db_rating.rating = rating.rating
            self.db.commit()
            self.db.refresh(db_rating)
        return db_rating

    def delete_rating(self, rating_id: int) -> bool:
        db_rating = self.db.query(RatingModel).filter(RatingModel.rating_id == rating_id).first()
        if db_rating:
            self.db.delete(db_rating)
            self.db.commit()
            return True
        return False