from sqlalchemy.orm import Session
from models.activity import Activity
from schemas.activity_schema import ActivityFilters


class ActivityRepo:
    @staticmethod
    def get_activity_by_id(db: Session, activity_id: int) -> Activity:
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def get_all_activities(db: Session, filters: ActivityFilters) -> list[Activity]:
        query = db.query(Activity)

        if filters.name:
            query = query.filter(Activity.name.ilike(f"%{filters.name}%"))  # Filtro "contains" para name
        if filters.date_from:
            query = query.filter(Activity.date >= filters.date_from)
        if filters.date_to:
            query = query.filter(Activity.date <= filters.date_to)
        if filters.cancelled is not None:
            query = query.filter(Activity.cancelled == filters.cancelled)
        if filters.place_id:
            query = query.filter(Activity.place_id == filters.place_id)
        if filters.organizer_id:
            query = query.filter(Activity.organizer_id == filters.organizer_id)

        if filters.is_date_order_asc:
            query = query.order_by(Activity.date.asc())
        else:
            query = query.order_by(Activity.date.desc())

        return query.all()

    @staticmethod
    def save_activity(db: Session, activity: Activity) -> Activity:
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def update_activity(db: Session, activity: Activity) -> Activity:
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def delete_activity(db: Session, activity: Activity):
        db.delete(activity)
        db.commit()


activity_repo: ActivityRepo = ActivityRepo()
