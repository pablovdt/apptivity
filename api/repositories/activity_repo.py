from sqlalchemy.orm import Session
from models.activity import Activity


class ActivityRepo:
    @staticmethod
    def save_activity(db: Session, activity: Activity) -> Activity:
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity


activity_repo: ActivityRepo = ActivityRepo()
