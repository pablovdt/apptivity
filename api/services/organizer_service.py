from sqlalchemy.orm import Session

from models import Activity
from models.organizer import Organizer
from schemas.organizer_schema import OrganizerCreate, OrganizerUpdate, OrganizerOut
from api.repositories.organizer_repo import organizer_repo, OrganizerRepo
from api.repositories.activity_repo import ActivityRepo, activity_repo


class OrganizerService:
    _repo: OrganizerRepo = organizer_repo
    _activity_repo: ActivityRepo = activity_repo

    def create_organizer(self, db: Session, organizer_create: OrganizerCreate) -> Organizer:
        organizer = Organizer(
            name=organizer_create.name,
            city_id=organizer_create.city_id,
            description=organizer_create.description,
            email=organizer_create.email,
            phone=organizer_create.phone,
            password=organizer_create.password,
            image_path=organizer_create.image_path
        )
        return self._repo.save_organizer(db=db, organizer=organizer)

    def get_organizer(self, db: Session, organizer_id: int) -> OrganizerOut:
        organizer = self._repo.get_organizer(db=db, organizer_id=organizer_id)
        if organizer:
            return organizer
        else:
            raise ValueError("Organizer not found")

    def get_all_organizers(self, db: Session, filters: dict = None) -> list[Organizer]:
        return self._repo.get_all_organizers(db=db, filters=filters)

    def update_organizer(self, db: Session, organizer_id: int, organizer_update: OrganizerUpdate) -> Organizer:
        organizer_data = organizer_update.dict(exclude_unset=True)
        updated_organizer = self._repo.update_organizer(db=db, organizer_id=organizer_id, organizer_data=organizer_data)
        if updated_organizer:
            return updated_organizer
        else:
            raise ValueError("Organizer not found")

    def delete_organizer(self, db: Session, organizer_id: int):
        # Check if the organizer has any associated activities
        if db.query(Activity).filter(Activity.organizer_id == organizer_id).first():
            raise ValueError("Cannot delete organizer because it has associated activities")
        self._repo.delete_organizer(db=db, organizer_id=organizer_id)

    def get_password_by_email(self, db: Session, email: str) -> str:
        password = self._repo.get_password_by_email(db=db, email=email)
        if password:
            return password
        else:
            raise ValueError("No se encuentra un organizador con este email")

    def get_organizer_by_email(self, db: Session, email: str) -> OrganizerOut:
        organizer = self._repo.get_organizer_by_email(db=db, email=email)
        if organizer:
            return organizer
        else:
            raise ValueError("No se encuentra un organizador cone este email")

    def get_coordinates_from_users(self, db: Session, organizer_id: int)-> list[dict]:
        return self._repo.get_coordinates_from_users(db, organizer_id)


organizer_service: OrganizerService = OrganizerService()
