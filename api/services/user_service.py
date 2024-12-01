from sqlalchemy.orm import Session
from datetime import datetime
from models import Activity
from models.user import User
from schemas.activity_schema import ActivityForUserOut
from schemas.user_schema import UserCreate, UserUpdate
from api.repositories.user_repo import user_repo, UserRepo
from api.services.category_service import category_service
from sqlalchemy import update
from models.user_activity import user_activity
from api.services.organizer_service import organizer_service

class UserService:
    _repo: UserRepo = user_repo
    _category_service = category_service
    _organizer_service = organizer_service

    def create_user(self, db: Session, user_create: UserCreate) -> User:
        user = User(
            name=user_create.name,
            email=user_create.email,
            password=user_create.password,
            city_id=user_create.city_id,
            notification_distance=user_create.notification_distance,
            settings=user_create.settings
        )
        category_ids = []
        if user_create.category_ids:
            categories = []

            for category_id in user_create.category_ids:
                category = category_service.get_category(db=db, category_id=category_id)
                categories.append(category)
                category_ids.append(category.id)

            user.categories = categories

        user = self._repo.save_user(db=db, user=user)

        if category_ids:

            activities = (
                db.query(Activity)
                .filter(
                    Activity.category_id.in_(category_ids),
                    Activity.date >= datetime.utcnow()
                )
                .all()
            )

            for activity in activities:
                db.execute(
                    user_activity.insert().values(
                        user_id=user.id,
                        activity_id=activity.id,
                        assistance=None,
                        inserted=datetime.utcnow(),
                        updated=datetime.utcnow()
                    )
                )

            db.commit()
            db.refresh(user)

        return user

    def get_user(self, db: Session, user_id: int) -> User:
        user = self._repo.get_user(db=db, user_id=user_id)
        if user:
            return user
        else:
            raise ValueError("User not found")

    def get_all_users(self, db: Session, filters: dict = None) -> list[User]:
        return self._repo.get_all_users(db=db, filters=filters)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> User:
        # todo, cambiar por         user = self._repo.get_user(db=db, user_id=user_id) ?????
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise ValueError("User not found")

        if user_update.name is not None:
            user.name = user_update.name
        if user_update.email is not None:
            user.email = user_update.email
        if user_update.password is not None:
            user.password = user_update.password
        if user_update.city_id is not None:
            user.city_id = user_update.city_id
        if user_update.notification_distance is not None:
            user.notification_distance = user_update.notification_distance
        if user_update.settings is not None:
            user.settings = user_update.settings

        if user_update.categories is not None:
            user.categories.clear()

            categories = []
            category_ids = []
            for category_id in user_update.categories:
                category = category_service.get_category(db=db, category_id=category_id)
                categories.append(category)
                category_ids.append(category.id)

            user.categories = categories

            activities = (
                db.query(Activity)
                .filter(
                    Activity.category_id.in_(category_ids),
                    Activity.date >= datetime.utcnow()
                )
                .all()
            )

            user.activities.clear()
            db.commit()
            db.refresh(user)

            for activity in activities:
                db.execute(
                    user_activity.insert().values(
                        user_id=user.id,
                        activity_id=activity.id,
                        assistance=None,
                        inserted=datetime.utcnow(),
                        updated=datetime.utcnow()
                    )
                )

        db.commit()
        db.refresh(user)

        return user

    def delete_user(self, db: Session, user_id: int):
        self._repo.delete_user(db=db, user_id=user_id)


    def get_password_by_email(self, db: Session, email: str) -> str:
        password = self._repo.get_password_by_email(db=db, email=email)
        if password:
            return password
        else:
            raise ValueError("No se encuentra un organizador con este email")

    def get_user_by_email(self, db: Session, email: str) -> User:
        user = self._repo.get_user_by_email(db=db, email=email)
        if user:
            return user
        else:
            raise ValueError("No se encuentra un organizador cone este email")

    # def get_user_activities(self, db: Session, user_id: int) -> list[Activity]:
    #
    #     user = self._repo.get_user(db=db, user_id=user_id)
    #     if not user:
    #         raise ValueError("User not found")
    #
    #     return user.activities

    def get_user_activities(self, db, user_id: int):
        activities_data = self._repo.get_user_activities(db=db, user_id=user_id)

        activities_list = []

        for activity, assistance in activities_data:

            organizer_name = self._organizer_service.get_organizer(db, activity.organizer_id).name

            activity_out = ActivityForUserOut(
                id=activity.id,
                name=activity.name,
                place_id=activity.place_id,
                date=activity.date,
                price=activity.price,
                organizer_id=activity.organizer_id,
                organizer_name=organizer_name,
                description=activity.description,
                image_path=activity.image_path,
                category_id=activity.category_id,
                cancelled=activity.cancelled,
                assistance=assistance
            )

            activities_list.append(activity_out)

        return activities_list

    def update_assistance(self, db: Session, user_id: int, activity_id: int, assistance):
        user = self._repo.get_user(db=db, user_id=user_id)
        if not user:
            raise ValueError("User not found")

        for activity in user.activities:
            if activity.id == activity_id:
                db.execute(
                    update(user_activity)
                    .where(
                        user_activity.c.user_id == user_id,
                        user_activity.c.activity_id == activity_id
                    )
                    .values(assistance=assistance, updated=datetime.utcnow())
                )
                db.commit()
                return {"assistance": assistance}

        raise ValueError("Actividad no encontrada para el usuario.")

user_service: UserService = UserService()
