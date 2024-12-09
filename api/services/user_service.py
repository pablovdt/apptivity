from sqlalchemy.orm import Session
from datetime import datetime
import re
from api.repositories.organizer_repo import OrganizerRepo
from api.services.place_service import place_service
from models import Activity, Organizer
from models.user import User
from schemas.activity_schema import ActivityForUserOut, ActivityFilters
from schemas.user_schema import UserCreate, UserUpdate, UserActivityFilters, UserMoreActivitiesIn, ValidateQrLocation
from api.repositories.user_repo import user_repo, UserRepo
from api.services.category_service import category_service
from sqlalchemy import update
from models.user_activity import user_activity
from api.services.organizer_service import organizer_service
from api.services.city_service import city_service
from core.haversine import haversine
from models.user_organizer import user_organizer


class UserService:
    _repo: UserRepo = user_repo
    _activity_service = None
    _category_service = category_service
    _organizer_service = organizer_service
    _city_service = city_service
    _place_service = place_service

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

                # calculo de la distancia entre el usuario y la acticvidad

                user_city = self._city_service.get_city_by_id(db=db, city_id=user.city_id)
                organizer = self._organizer_service.get_organizer(db=db, organizer_id=activity.organizer_id)
                organizer_city = self._city_service.get_city_by_id(db=db, city_id=organizer.city_id)

                distance_between_user_and_activity = haversine(user_city.latitude,
                                                               user_city.longitude,
                                                               organizer_city.latitude,
                                                               organizer_city.longitude)

                if distance_between_user_and_activity < user.notification_distance:
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

    def add_user_activity(self, db: Session, user_id: int, activity_id: int):
        user = self._repo.get_user(db=db, user_id=user_id)

        if not user:
            raise ValueError("User not found")

        db.execute(
            user_activity.insert().values(
                user_id=user.id,
                activity_id=activity_id,
                assistance=None,
                inserted=datetime.utcnow(),
                updated=datetime.utcnow()
            )
        )

        db.commit()
        db.refresh(user)

    def add_user_organizer(self, user_id: int, organizer_id: int, db: Session):
        # add user and organizer in user_organizer table
        user = self._repo.get_user(db=db, user_id=user_id)

        if not user:
            raise ValueError("User not found")

        db.execute(
            user_organizer.insert().values(
                user_id=user.id,
                organizer_id=organizer_id,
                inserted=datetime.utcnow(),
                updated=datetime.utcnow()
            )
        )

        # insert all activities from organizer in user_activities
        from api.services.activity_service import activity_service
        self._activity_service = activity_service
        activity_filters: ActivityFilters = ActivityFilters()
        activity_filters.organizer_id = organizer_id
        activity_filters.date_from = datetime.now()
        organizer_activities = self._activity_service.get_all_activities(db=db, filters=activity_filters)

        for activity in organizer_activities:
            user_activity_ids = [activity.id for activity in user.activities]

            if activity.id not in user_activity_ids:
                self.add_user_activity(db=db, user_id=user_id, activity_id=activity.id)

        db.commit()
        db.refresh(user)

    def get_user(self, db: Session, user_id: int) -> User:
        user = self._repo.get_user(db=db, user_id=user_id)
        if user:
            return user
        else:
            raise ValueError("User not found")

    def get_all_users(self, db: Session, filters: dict = None) -> list[User]:
        return self._repo.get_all_users(db=db, filters=filters)

    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> User:

        user = user_service.get_user(db=db, user_id=user_id)

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

        if len(user_update.categories) > 0:
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

                # calculo de la distancia entre el usuario y la acticvidad

                user_city = city_service.get_city_by_id(db=db, city_id=user.city_id)
                organizer = organizer_service.get_organizer(db=db, organizer_id=activity.organizer_id)
                organizer_city = city_service.get_city_by_id(db=db, city_id=organizer.city_id)

                distance_between_user_and_activity = haversine(user_city.latitude,
                                                               user_city.longitude,
                                                               organizer_city.latitude,
                                                               organizer_city.longitude)

                if distance_between_user_and_activity < user.notification_distance:
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

    def get_user_activities(self, db, user_id: int, filters: UserActivityFilters):
        activities_data = self._repo.get_user_activities(db=db, user_id=user_id, filters=filters)

        activities_list = []

        for activity, possible_assistance, assistance in activities_data:
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
                possible_assistance=possible_assistance,
                assistance=assistance
            )

            activities_list.append(activity_out)

        return activities_list

    def get_user_organizers(self, db, user_id: int):
        return self._repo.get_user_organizers(db=db, user_id=user_id)

    def get_activities_updated(self, user_id: int, db: Session):
        # Consulta las actividades cuyo updated_confirmed sea False para el usuario dado
        query = db.query(Activity.id, Activity.name) \
            .join(user_activity, user_activity.c.activity_id == Activity.id) \
            .filter(user_activity.c.user_id == user_id) \
            .filter(user_activity.c.updated_confirmed == False)

        # Obtén todas las actividades que cumplen con el criterio
        activities = query.all()

        # Si no hay actividades, devuelve una lista vacía
        activities_list = [{"activity_id": activity.id, "name": activity.name} for activity in activities]

        return activities_list

    def get_user_more_activities(self, db, user_more_activities: UserMoreActivitiesIn):
        activities_data = self._repo.get_user_more_activities(db=db, user_more_activities=user_more_activities)

        activities_list = []

        for activity in activities_data:
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
                assistance=None
            )

            activities_list.append(activity_out)

        return activities_list

    def update_possible_assistance(self, db: Session, user_id: int, activity_id: int, possible_assistance: bool):
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
                    .values(possible_assistance=possible_assistance, updated=datetime.utcnow())
                )
                db.commit()
                return {"posible assistance": possible_assistance}

        raise ValueError("Actividad no encontrada para el usuario.")

    def update_activity_updated_confirmed(self, db: Session, user_id: int, activity_id: int, updated_confirmed: bool):

        stmt = (
            update(user_activity)
            .where(
                (user_activity.c.user_id == user_id) &
                (user_activity.c.activity_id == activity_id)
            )
            .values(
                updated_confirmed=updated_confirmed,
                updated=datetime.utcnow()
            )
        )
        db.execute(stmt)
        db.commit()

        return {f"updated confirmed in activity {activity_id} for user {user_id}": updated_confirmed}

    def update_assistance(self, db: Session, user_id: int, activity_id: int, assistance: bool):
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


    def validate_qr_and_location(self, db: Session, validate_qr_and_location: ValidateQrLocation) -> bool:
        from api.services.activity_service import activity_service
        self._activity_service = activity_service
        activity = self._activity_service.get_activity(db=db, activity_id=validate_qr_and_location.activity_id)

        place = self._place_service.get_place(db=db, place_id=activity.place_id)

        pattern = r"q=([\-+]?[0-9]*\.?[0-9]+),([\-+]?[0-9]*\.?[0-9]+)"
        match = re.search(pattern, place.location_url)

        if match:
            place_latitude = float(match.group(1))
            place_longitude = float(match.group(2))
        else:
            return False

        # comprobacion de la distancia entre el usuario escaneando el qr y la geolocalizacion de la actividad

        distance = haversine(lat1=validate_qr_and_location.latitude,
                             lon1=validate_qr_and_location.longitude,
                             lat2=place_latitude,
                             lon2=place_longitude
                             )
        # 100 m
        if distance <= 0.1:
            self.update_assistance(db=db, user_id=validate_qr_and_location.user_id, activity_id=activity.id,
                                   assistance=True)
            return True
        else:
            return False

    def get_assistances(self, db: Session, user_id: int):
        return self._repo.get_assistances(db=db, user_id=user_id)

user_service: UserService = UserService()
