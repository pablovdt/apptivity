from sqlalchemy.orm import Session
from models.organizer import Organizer

class OrganizerRepo:
    @staticmethod
    def save_organizer(db: Session, organizer: Organizer) -> Organizer:
        db.add(organizer)
        db.commit()
        db.refresh(organizer)
        return organizer

organizer_repo: OrganizerRepo = OrganizerRepo()
