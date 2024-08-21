from sqlalchemy.orm import Session
from models.organizer import Organizer
from schemas.organizer_schema import OrganizerCreate
from api.repositories.organizer_repo import organizer_repo, OrganizerRepo


class OrganizerService:
    _repo: OrganizerRepo = organizer_repo

    def create_organizer(self, db: Session, organizer_create: OrganizerCreate) -> Organizer:
        if db.query(Organizer).filter(Organizer.email == organizer_create.email).first():
            raise ValueError("El correo electrónico ya está registrado")

        organizer = Organizer(
            name=organizer_create.name,
            city_cp=organizer_create.city_cp,
            description=organizer_create.description,
            email=organizer_create.email,
            phone=organizer_create.phone
        )

        return self._repo.save_organizer(db=db, organizer=organizer)


organizer_service: OrganizerService = OrganizerService()
