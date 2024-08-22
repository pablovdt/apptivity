from sqlalchemy.orm import Session
from models.organizer import Organizer


class OrganizerRepo:
    @staticmethod
    def save_organizer(db: Session, organizer: Organizer) -> Organizer:
        db.add(organizer)
        db.commit()
        db.refresh(organizer)
        return organizer

    @staticmethod
    def get_organizer(db: Session, organizer_id: int) -> Organizer:
        return db.query(Organizer).filter(Organizer.id == organizer_id).first()

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
    def get_organizer_by_email(db: Session, email: str) -> Organizer:
        return db.query(Organizer).filter(Organizer.email == email).first()


organizer_repo: OrganizerRepo = OrganizerRepo()
