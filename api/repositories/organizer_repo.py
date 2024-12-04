from sqlalchemy.orm import Session
from sqlalchemy import select, distinct, join, and_
from sqlalchemy.testing.suite.test_reflection import users

from models import Activity, City, User
from models.organizer import Organizer
from models.user_activity import user_activity
from schemas.category_schema import CategoryOut
from schemas.organizer_schema import OrganizerOut
from schemas.user_schema import UserOut


class OrganizerRepo:
    @staticmethod
    def save_organizer(db: Session, organizer: Organizer) -> Organizer:
        db.add(organizer)
        db.commit()
        db.refresh(organizer)
        return organizer

    @staticmethod
    def get_organizer(db: Session, organizer_id: int) -> OrganizerOut:
        result = db.query(Organizer, City.latitude, City.longitude).join(City).filter(
            Organizer.id == organizer_id).first()

        if result:
            organizer, latitude, longitude = result

            users = [
                UserOut(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    city_id=user.city_id,
                    settings=user.settings,
                    notification_distance=user.notification_distance,
                    categories=[
                        CategoryOut(id=category.id, name=category.name)
                        for category in user.categories
                    ]
                )
                for user in organizer.users
            ]

            return OrganizerOut(
                id=organizer.id,
                name=organizer.name,
                city_id=organizer.city_id,
                description=organizer.description,
                password=organizer.password,
                email=organizer.email,
                phone=organizer.phone,
                image_path=organizer.image_path,
                city_latitude=latitude,
                city_longitude=longitude,
                users=users
            )

    @staticmethod
    def get_all_organizers(db: Session, filters: dict = None) -> list[Organizer]:
        query = db.query(Organizer)
        if filters:
            for key, value in filters.items():
                if key in ["name"]:
                    query = query.filter(getattr(Organizer, key).ilike(f"%{value}%"))
                else:
                    query = query.filter(getattr(Organizer, key) == value)
        return query.all()

    @staticmethod
    def update_organizer(db: Session, organizer_id: int, organizer_data: dict) -> Organizer:
        organizer = db.query(Organizer).filter(Organizer.id == organizer_id).first()
        if organizer:
            for key, value in organizer_data.items():
                setattr(organizer, key, value)
            db.commit()
            db.refresh(organizer)
            return organizer
        else:
            return None

    @staticmethod
    def delete_organizer(db: Session, organizer_id: int):
        organizer = db.query(Organizer).filter(Organizer.id == organizer_id).first()
        if organizer:
            db.delete(organizer)
            db.commit()
        else:
            raise ValueError("Organizer not found")

    @staticmethod
    def get_password_by_email(db: Session, email: str) -> str:
        organizer = db.query(Organizer).filter(Organizer.email == email).first()
        if organizer:
            return organizer.password
        else:
            return None

    @staticmethod
    def get_organizer_by_email(db: Session, email: str) -> OrganizerOut:
        result = db.query(Organizer, City.latitude, City.longitude).join(City).filter(
            Organizer.email == email).first()

        if result:
            organizer, latitude, longitude = result

            return OrganizerOut(
                id=organizer.id,
                name=organizer.name,
                city_id=organizer.city_id,
                description=organizer.description,
                password=organizer.password,
                email=organizer.email,
                phone=organizer.phone,
                image_path=organizer.image_path,
                city_latitude=latitude,
                city_longitude=longitude
            )

    @staticmethod
    def get_coordinates_from_users(db: Session, organizer_id: int) -> list[dict]:

        subquery = db.query(Activity.id).filter(Activity.organizer_id == organizer_id).subquery()

        result = db.query(User.id).distinct().join(user_activity, user_activity.c.user_id == User.id) \
            .filter(user_activity.c.activity_id.in_(subquery)).all()

        user_ids = [user.id for user in result]

        city_coordinates = db.query(City.latitude, City.longitude, City.name).distinct() \
            .join(User, User.city_id == City.id) \
            .filter(User.id.in_(user_ids)) \
            .all()

        coordinates_dict = [{'latitude': latitude, 'longitude': longitude,'city_name':city_name,} for latitude, longitude, city_name in city_coordinates]

        return coordinates_dict


organizer_repo: OrganizerRepo = OrganizerRepo()
