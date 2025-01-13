from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Tag(Base):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id", ondelete="CASCADE"), nullable=False)
    tag = Column(String, nullable=False)