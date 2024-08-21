from sqlalchemy.orm import Session
from models.place import Place
from schemas.place_schema import PlaceCreate
from api.repositories.place_repo import place_repo, PlaceRepo


class PlaceService:
    _repo: PlaceRepo = place_repo

    def create_place(self, db: Session, place_create: PlaceCreate) -> Place:
        place = Place(
            name=place_create.name,
            city_cp=place_create.city_cp
        )

        return self._repo.save_place(db=db, place=place)


place_service: PlaceService = PlaceService()
