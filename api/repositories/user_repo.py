from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, Integer, select
from api.services.category_service import category_service
from models import Category, Organizer
from models.user import User
from typing import Optional
from models.user_activity import user_activity
from models.activity import Activity
from schemas.category_schema import CategoryOut
from schemas.user_schema import UserActivityFilters, UserMoreActivitiesIn, UserOut
from datetime import datetime
from models.user_organizer import user_organizer
from sqlalchemy import func
import random

class UserRepo:
    @staticmethod
    def save_user(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    # @staticmethod
    # def get_user(db: Session, user_id: int) -> Optional[User]:
    #     return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:

        user = (
            db.query(User)
            .options(joinedload(User.level), joinedload(User.categories))
            .filter(User.id == user_id)
            .one_or_none()
        )

        if not user:
            raise ValueError(f"Usuario con ID {user_id} no encontrado")

        categories_out = [
            CategoryOut(id=category.id, name=category.name)
            for category in user.categories
        ]
        return user
        # return UserOut(
        #     id=user.id,
        #     name=user.name,
        #     email=user.email,
        #     city_id=user.city_id,
        #     settings=user.settings,
        #     notification_distance=user.notification_distance,
        #     categories=categories_out,
        #     points=user.points,
        #     level_id=user.level_id,
        #     level_name=user.level.name
        # )

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
    def get_user_by_email(db: Session, email: str) -> UserOut:
        user = (
            db.query(User)
            .options(joinedload(User.level), joinedload(User.categories))
            .filter(User.email == email)
            .one_or_none()
        )

        if not user:
            raise ValueError(f"Usuario con email {email} no encontrado")

        categories_out = [
            CategoryOut(id=category.id, name=category.name)
            for category in user.categories
        ]
        return user
        # return UserOut(
        #     id=user.id,
        #     name=user.name,
        #     email=user.email,
        #     city_id=user.city_id,
        #     settings=user.settings,
        #     notification_distance=user.notification_distance,
        #     categories=categories_out,
        #     points=user.points,
        #     level_id=user.level_id,
        #     level_name=user.level.name
        # )

    @staticmethod
    def get_user_activities(db: Session, user_id: int, filters: UserActivityFilters):

        query = db.query(Activity, user_activity.c.possible_assistance, user_activity.c.assistance) \
            .join(user_activity, user_activity.c.activity_id == Activity.id) \
            .filter(user_activity.c.user_id == user_id)

        if not filters.all:
            query = query.filter(
                or_(user_activity.c.possible_assistance == True, user_activity.c.possible_assistance == None)
            )

        if filters.name:
            query = query.filter(Activity.name.ilike(f"%{filters.name}%"))
        if filters.date_from:
            query = query.filter(Activity.date >= filters.date_from)
        if filters.date_to:
            query = query.filter(Activity.date <= filters.date_to)
        if filters.organizer_id:
            query = query.filter(Activity.organizer_id == filters.organizer_id)
        if filters.cancelled is not None:
            query = query.filter(Activity.cancelled == filters.cancelled)

        if filters.is_date_order_asc:
            query = query.order_by(Activity.date.asc())
        else:
            query = query.order_by(Activity.date.desc())

        return query.all()

    from datetime import datetime

    @staticmethod
    def get_user_more_activities(db: Session, user_more_activities: UserMoreActivitiesIn):

        # Actividades del usuario
        user_activities_subquery = (
            select(user_activity.c.activity_id)
            .where(user_activity.c.user_id == user_more_activities.user_id)
        )


        query = (
            db.query(Activity)
            .filter(~Activity.id.in_(user_activities_subquery))
            .filter(Activity.date > datetime.now())
            .order_by(func.random())
            .limit(20)
        )

        # Ejecutar y devolver las actividades
        return query.all()

    @staticmethod
    def get_user_organizers(db: Session, user_id: int):

        query = db.query(Organizer) \
            .join(user_organizer, user_organizer.c.organizer_id == Organizer.id) \
            .filter(user_activity.c.user_id == user_id)

        return query.all()

    @staticmethod
    def get_assistances(db: Session, user_id: int):

        total_assistance = db.query(func.sum(user_activity.c.assistance.cast(Integer)).label('total_assistance')) \
            .filter(user_activity.c.user_id == user_id) \
            .scalar()

        return total_assistance if total_assistance is not None else 0


user_repo: UserRepo = UserRepo()
