from sqlalchemy.orm import Session

from api.services.city_service import city_service
from api.services.organizer_service import organizer_service
from core.haversine import haversine
from models.activity import Activity
from schemas.activity_schema import ActivityCreate, ActivityUpdate, ActivityFilters
from api.repositories.activity_repo import activity_repo, ActivityRepo
from api.services.user_service import user_service
from typing import Dict
from datetime import datetime
from models.user_activity import user_activity


class ActivityService:
    _repo: ActivityRepo = activity_repo
    _user_service = user_service
    _organizer_service = organizer_service
    _city_service = city_service

    def create_activity(self, db: Session, activity_create: ActivityCreate) -> Activity:
        activity = Activity(
            name=activity_create.name,
            place_id=activity_create.place_id,
            date=activity_create.date,
            price=activity_create.price,
            organizer_id=activity_create.organizer_id,
            description=activity_create.description,
            image_path=activity_create.image_path if activity_create.image_path else "images/logotipo_apptivity.png",
            category_id=activity_create.category_id,
            cancelled=activity_create.cancelled,
            number_of_assistances=activity_create.number_of_assistances,
            number_of_shipments=activity_create.number_of_shipments,
            number_of_discards=activity_create.number_of_discards
        )

        activity_saved = self._repo.save_activity(db=db, activity=activity)

        users = self._user_service.get_all_users(db=db)
        for user in users:
            user_city = city_service.get_city_by_id(db=db, city_id=user.city_id)
            organizer = organizer_service.get_organizer(db=db, organizer_id=activity.organizer_id)
            organizer_city = city_service.get_city_by_id(db=db, city_id=organizer.city_id)

            distance_between_user_and_activity = haversine(user_city.latitude,
                                                           user_city.longitude,
                                                           organizer_city.latitude,
                                                           organizer_city.longitude)

            # la actividad creada se le asigna a un usuario depende de:
            #   Si la categoria de la actividad es igual a una categoria del usuario y la distancia es menor
            #   O si estas suscrito
            if (
                    (distance_between_user_and_activity < user.notification_distance and
                     any(category.id == activity.category_id for category in user.categories)) or
                    any(u.id == user.id for u in organizer.users)
            ):
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
        db.refresh(activity)

        return activity_saved

    def get_activity(self, db: Session, activity_id: int) -> Activity:
        activity = self._repo.get_activity_by_id(db=db, activity_id=activity_id)
        if not activity:
            raise ValueError("La actividad no existe")
        return activity

    def get_all_activities(self, db: Session, filters: ActivityFilters) -> list[Activity]:
        return self._repo.get_all_activities(db=db, filters=filters)

    def get_activities_by_month(self, db: Session, organizer_id: int, year: int) -> Dict[str, int]:

        activities_by_month = self._repo.get_activities_by_month(db, organizer_id, year)

        months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        result = {month: 0 for month in months}

        for activity in activities_by_month:
            month_number = int(activity.month)
            if 1 <= month_number <= 12:
                month_name = months[month_number - 1]
                result[month_name] += activity.activity_count

        return result

    def update_activity(self, db: Session, activity_id: int, activity_update: ActivityUpdate) -> Activity:
        activity = self.get_activity(db=db, activity_id=activity_id)
        for key, value in activity_update.dict(exclude_unset=True).items():
            setattr(activity, key, value)
        return self._repo.update_activity(db=db, activity=activity)

    def delete_activity(self, db: Session, activity_id: int):
        activity = self.get_activity(db=db, activity_id=activity_id)
        self._repo.delete_activity(db=db, activity=activity)


activity_service: ActivityService = ActivityService()
