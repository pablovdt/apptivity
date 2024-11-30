from sqlalchemy.orm import Session

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
        user_data = user_update.dict(exclude_unset=True)
        updated_user = self._repo.update_user(db=db, user_id=user_id, user_data=user_data)
        if updated_user:
            return updated_user
        else:
            raise ValueError("User not found")

    def delete_user(self, db: Session, user_id: int):
        self._repo.delete_user(db=db, user_id=user_id)


user_service: UserService = UserService()
