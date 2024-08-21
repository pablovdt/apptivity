from sqlalchemy.orm import Session
from models.activity import Activity
from schemas.activity_schema import ActivityCreate
from api.repositories.activity_repo import activity_repo, ActivityRepo


class ActivityService:
    _repo: ActivityRepo = activity_repo

    def create_activity(self, db: Session, activity_create: ActivityCreate) -> Activity:
        activity = Activity(
            name=activity_create.name,
            city_cp=activity_create.city_cp,
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


activity_service: ActivityService = ActivityService()
