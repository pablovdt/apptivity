from sqlalchemy.orm import Session

from models import Activity
from models.user import User
from schemas.user_schema import UserCreate, UserUpdate
from api.repositories.user_repo import user_repo, UserRepo
from api.repositories.activity_repo import ActivityRepo


class UserService:
    _repo: UserRepo = user_repo
    _activity_repo = ActivityRepo()

    def create_user(self, db: Session, user_create: UserCreate) -> User:
        user = User(
            name=user_create.name,
            email=user_create.email,
            password=user_create.password,  # Asegúrate de hashear la contraseña antes de guardarla
            city_cp=user_create.city_cp,
            settings=user_create.settings
        )
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
        # Check if the user has any associated activities
        if db.query(Activity).filter(Activity.user_id == user_id).first():
            raise ValueError("Cannot delete user because it has associated activities")

        # If no associated activities, proceed to delete the user
        self._repo.delete_user(db=db, user_id=user_id)


user_service: UserService = UserService()
