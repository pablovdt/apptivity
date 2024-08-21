from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from core.security import get_password_hash
from api.repositories.user_repo import UserRepo
from api.repositories.user_repo import user_repo


class UserService:
    _repo: UserRepo = user_repo

    def create_user(self, db: Session, user_create: UserCreate) -> User:
        if db.query(User).filter(User.email == user_create.email).first():
            raise ValueError("El correo electrónico ya está registrado")

        hashed_password = get_password_hash(user_create.password)
        user = User(
            name=user_create.name,
            email=user_create.email,
            password=hashed_password,
            city_cp=user_create.city_cp,
            settings=user_create.settings
        )

        return self._repo.save_user(db=db, user=user)


user_service: UserService = UserService()
