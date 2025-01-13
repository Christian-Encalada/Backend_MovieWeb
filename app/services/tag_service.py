from sqlalchemy.orm import Session
from app.models.tag import Tag as TagModel
from app.schemas.tag import TagCreate, Tag as TagSchema

class TagService:
    def __init__(self, db: Session):
        self.db = db

    def create_tag(self, tag: TagCreate) -> TagSchema:
        db_tag = TagModel(movie_id=tag.movie_id, tag=tag.tag)
        self.db.add(db_tag)
        self.db.commit()
        self.db.refresh(db_tag)
        return db_tag

    def get_tag(self, tag_id: int) -> TagSchema:
        return self.db.query(TagModel).filter(TagModel.tag_id == tag_id).first()

    def get_all_tags(self) -> list[TagSchema]:
        return self.db.query(TagModel).all()

    def update_tag(self, tag_id: int, tag: TagCreate) -> TagSchema:
        db_tag = self.db.query(TagModel).filter(TagModel.tag_id == tag_id).first()
        if db_tag:
            db_tag.movie_id = tag.movie_id
            db_tag.tag = tag.tag
            self.db.commit()
            self.db.refresh(db_tag)
        return db_tag

    def delete_tag(self, tag_id: int) -> bool:
        db_tag = self.db.query(TagModel).filter(TagModel.tag_id == tag_id).first()
        if db_tag:
            self.db.delete(db_tag)
            self.db.commit()
            return True
        return False