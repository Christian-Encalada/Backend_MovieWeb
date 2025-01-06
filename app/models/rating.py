from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    movie_id = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)

    user = relationship("User", back_populates="ratings")