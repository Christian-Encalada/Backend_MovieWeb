from sqlalchemy import Column, Integer, Float, ForeignKey
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)