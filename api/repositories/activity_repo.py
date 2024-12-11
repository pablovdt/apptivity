from sqlalchemy.orm import Session

from models import City, Place
from models.activity import Activity
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from collections import namedtuple
from schemas.activity_schema import ActivityFilters

ActivityMonth = namedtuple("ActivityMonth", ["month", "activity_count"])


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


        # todo, change filter name to number_of_possible_assistances
        if filters.order_by_assistance:
            query = query.order_by(Activity.number_of_possible_assistances.desc())

        if filters.is_date_order_asc:
            query = query.order_by(Activity.date.asc())
        else:
            query = query.order_by(Activity.date.desc())

        if filters.organizer_id:
            query = query.filter(Activity.organizer_id == filters.organizer_id)

        if filters.limit:
            query = query.limit(filters.limit)

        return query.all()

    @staticmethod
    def get_activities_by_city( db: Session, city_id:int):
        query = db.query(Activity).join(Place).join(City).filter(City.id == city_id)

        activities = query.all()
        return activities

    @staticmethod
    def get_activities_by_month(db: Session, organizer_id: int, year: int):

        query = db.query(
            extract('month', Activity.date).label('month'),
            func.count(Activity.id).label('activity_count')
        ).filter(
            Activity.organizer_id == organizer_id,
            extract('year', Activity.date) == year
        ).group_by(
            extract('month', Activity.date)
        ).order_by(
            extract('month', Activity.date)
        )

        result = query.all()

        return [ActivityMonth(month=month, activity_count=activity_count) for month, activity_count in result]

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
