from sqlalchemy.orm import Session
from models.activity import Activity


class ActivityRepo:
    @staticmethod
    def get_activity_by_id(db: Session, activity_id: int) -> Activity:
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def get_all_activities(db: Session, filters: dict = None) -> list[Activity]:
        query = db.query(Activity)

        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(Activity, key) == value)

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
