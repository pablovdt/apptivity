from sqlalchemy.orm import Session
from models.user import User
from typing import Optional

class UserRepo:
    @staticmethod
    def save_user(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_all_users(db: Session, filters: dict = None) -> list[User]:
        query = db.query(User)
        if filters:
            for key, value in filters.items():
                if key in ["name", "email"]:
                    query = query.filter(getattr(User, key).ilike(f"%{value}%"))
                else:
                    query = query.filter(getattr(User, key) == value)
        return query.all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: dict) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return user
        else:
            return None

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        else:
            raise ValueError("User not found")

user_repo: UserRepo = UserRepo()
