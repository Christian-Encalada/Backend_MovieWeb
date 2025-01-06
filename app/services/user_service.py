from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, User as UserSchema

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserSchema:
        db_user = UserModel(name=user.name, email=user.email, password=user.password, favs=user.favs)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: int) -> UserSchema:
        return self.db.query(UserModel).filter(UserModel.user_id == user_id).first()

    def get_all_users(self) -> list[UserSchema]:
        return self.db.query(UserModel).all()

    def update_user(self, user_id: int, user: UserCreate) -> UserSchema:
        db_user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if db_user:
            db_user.name = user.name
            db_user.email = user.email
            db_user.password = user.password
            db_user.favs = user.favs
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        db_user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False