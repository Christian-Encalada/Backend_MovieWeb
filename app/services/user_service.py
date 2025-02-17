from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, User as UserSchema, UserLogin
from app.core.security import verify_password, get_password_hash, create_access_token
from datetime import timedelta

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserSchema:
        # Verificar si el usuario ya existe
        if self.get_user_by_username(user.username):
            raise ValueError("Username already registered")
        if self.get_user_by_email(user.email):
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user.password)
        db_user = UserModel(
            username=user.username,
            email=user.email,
            password=hashed_password,
            favs=user.favs
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate_user(self, username: str, password: str):
        try:
            user = self.get_user_by_username(username)
            if not user:
                return None
            if not verify_password(password, user.password):
                return None

            token = create_access_token(
                data={
                    "sub": str(user.user_id),
                    "username": user.username,
                    "email": user.email
                }
            )

            return {
                "access_token": token,
                "token_type": "Bearer",
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "email": user.email
                }
            }
        except Exception as e:
            print(f"Error in authenticate_user: {str(e)}")
            return None

    def get_user_by_username(self, username: str):
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_user(self, user_id: int):
        try:
            user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
            if user:
                # Asegurarnos de que favs sea una lista
                if user.favs is None or not isinstance(user.favs, list):
                    user.favs = []
                    self.db.commit()
            return user
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

    def get_all_users(self) -> list[UserSchema]:
        return self.db.query(UserModel).all()

    def update_user(self, user_id: int, user: UserCreate) -> UserSchema:
        db_user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if db_user:
            db_user.username = user.username
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

    def add_to_favorites(self, user_id: int, movie_id: int):
        user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if user:
            current_favs = user.favs if isinstance(user.favs, list) else []
            if movie_id not in current_favs:
                current_favs.append(movie_id)
                user.favs = current_favs
                self.db.commit()
                self.db.refresh(user)
        return user

    def remove_from_favorites(self, user_id: int, movie_id: int):
        user = self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
        if user:
            current_favs = user.favs if isinstance(user.favs, list) else []
            if movie_id in current_favs:
                current_favs.remove(movie_id)
                user.favs = current_favs
                self.db.commit()
                self.db.refresh(user)
        return user

    def update_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        
        if not verify_password(current_password, user.password):
            return False
        
        user.password = get_password_hash(new_password)
        self.db.commit()
        return True