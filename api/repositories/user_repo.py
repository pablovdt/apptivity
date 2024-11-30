from sqlalchemy.orm import Session

from api.services.category_service import category_service
from models import Category
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
                elif key == "categories":  # Filtrar por categorías
                    query = query.filter(User.categories.any(Category.id.in_(value)))
                else:
                    query = query.filter(getattr(User, key) == value)
        return query.all()


    @staticmethod
    def update_user(db: Session, user_id: int, user_data: dict) -> Optional[User]:
        # Buscar al usuario por ID
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        for key, value in user_data.items():
            if key != "category_ids" and value is not None:
                setattr(user, key, value)

        if "category_ids" in user_data:
            category_ids = user_data["category_ids"]
            user.categories.clear()

            categories = []
            for category_id in category_ids:
                category = category_service.get_category(db=db, category_id=category_id)
                if category:
                    categories.append(category)
            user.categories.extend(categories)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        else:
            raise ValueError("User not found")

    @staticmethod
    def get_password_by_email(db: Session, email: str) -> str:
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user.password
        else:
            return None

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()


user_repo: UserRepo = UserRepo()
