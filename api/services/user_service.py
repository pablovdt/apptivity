from sqlalchemy.orm import Session
from datetime import datetime
from models import Activity
from models.user import User
from schemas.user_schema import UserCreate, UserUpdate
from api.repositories.user_repo import user_repo, UserRepo
from api.services.category_service import category_service


class UserService:
    _repo: UserRepo = user_repo
    _category_service = category_service

    def create_user(self, db: Session, user_create: UserCreate) -> User:
        user = User(
            name=user_create.name,
            email=user_create.email,
            password=user_create.password,
            city_id=user_create.city_id,
            notification_distance=user_create.notification_distance,
            settings=user_create.settings
        )

        if user_create.category_ids:
            categories = []
            for category_id in user_create.category_ids:
                category = category_service.get_category(db=db, category_id=category_id)
                categories.append(category)

            user.categories = categories

        return self._repo.save_user(db=db, user=user)

    def get_user(self, db: Session, user_id: int) -> User:
        user = self._repo.get_user(db=db, user_id=user_id)
        if user:
            return user
        else:
            raise ValueError("User not found")

    def get_all_users(self, db: Session, filters: dict = None) -> list[User]:
        return self._repo.get_all_users(db=db, filters=filters)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> User:

        existing_user = self._repo.get_user(db=db, user_id=user_id)

        if not existing_user:
            raise ValueError("User not found")

        current_category_ids = {category.id for category in existing_user.categories}

        user_data = user_update.dict(exclude_unset=True)
        updated_categories = set(user_data.get("category_ids", []))

        updated_user = self._repo.update_user(db=db, user_id=user_id, user_data=user_data)

        new_category_ids = updated_categories - current_category_ids

        if new_category_ids:

            activities = (
                db.query(Activity)
                .filter(
                    Activity.category_id.in_(new_category_ids),
                    Activity.date >= datetime.utcnow()
                )
                .all()
            )

            for activity in activities:
                existing_user.activities.append(activity)

            db.commit()
            db.refresh(existing_user)

        return updated_user

    def delete_user(self, db: Session, user_id: int):
        self._repo.delete_user(db=db, user_id=user_id)


user_service: UserService = UserService()
