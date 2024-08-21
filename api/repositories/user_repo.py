from sqlalchemy.orm import Session
from models.user import User


class UserRepo:

    @staticmethod
    def save_user(db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user


user_repo: UserRepo = UserRepo()
