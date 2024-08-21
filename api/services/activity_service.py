from sqlalchemy.orm import Session
from models.activity import Activity
from schemas.activity_schema import ActivityCreate, ActivityUpdate
from api.repositories.activity_repo import activity_repo, ActivityRepo


class ActivityService:
    _repo: ActivityRepo = activity_repo

    def create_activity(self, db: Session, activity_create: ActivityCreate) -> Activity:
        activity = Activity(
            name=activity_create.name,
            place_id=activity_create.place_id,
            date=activity_create.date,
            price=activity_create.price,
            organizer_id=activity_create.organizer_id,
            description=activity_create.description,
            category_id=activity_create.category_id,
            cancelled=activity_create.cancelled,
            number_of_assistances=activity_create.number_of_assistances,
            number_of_shipments=activity_create.number_of_shipments,
            number_of_discards=activity_create.number_of_discards
        )
        return self._repo.save_activity(db=db, activity=activity)

    def get_activity(self, db: Session, activity_id: int) -> Activity:
        activity = self._repo.get_activity_by_id(db=db, activity_id=activity_id)
        if not activity:
            raise ValueError("La actividad no existe")
        return activity

    def get_all_activities(self, db: Session, filters: dict = None) -> list[Activity]:
        query = db.query(Activity)

        if filters:
            for key, value in filters.items():
                if key == "name" and value:
                    query = query.filter(Activity.name.ilike(f"%{value}%"))  # Filtro "contains" para name
                elif key in ["cancelled"]:
                    query = query.filter(getattr(Activity, key) == value)
                else:
                    query = query.filter(getattr(Activity, key) == value)

        return query.all()

    def update_activity(self, db: Session, activity_id: int, activity_update: ActivityUpdate) -> Activity:
        activity = self.get_activity(db=db, activity_id=activity_id)
        for key, value in activity_update.dict(exclude_unset=True).items():
            setattr(activity, key, value)
        return self._repo.update_activity(db=db, activity=activity)

    def delete_activity(self, db: Session, activity_id: int):
        activity = self.get_activity(db=db, activity_id=activity_id)
        self._repo.delete_activity(db=db, activity=activity)


activity_service: ActivityService = ActivityService()
