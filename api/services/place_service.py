from sqlalchemy.orm import Session

from models import Activity
from models.place import Place
from schemas.place_schema import PlaceCreate, PlaceUpdate
from api.repositories.place_repo import place_repo, PlaceRepo
from api.repositories.activity_repo import ActivityRepo


class PlaceService:
    _repo: PlaceRepo = place_repo
    _activity_repo = ActivityRepo()

    def create_place(self, db: Session, place_create: PlaceCreate) -> Place:
        place = Place(
            name=place_create.name,
            location_url=place_create.location_url,
            city_id=place_create.city_id
        )
        return self._repo.save_place(db=db, place=place)

    def get_place(self, db: Session, place_id: int) -> Place:
        place = self._repo.get_place(db=db, place_id=place_id)
        if place:
            return place
        else:
            raise ValueError("Place not found")

    def get_all_places(self, db: Session, filters: dict = None) -> list[Place]:
        return self._repo.get_all_places(db=db, filters=filters)

    def update_place(self, db: Session, place_id: int, place_update: PlaceUpdate) -> Place:
        place_data = place_update.dict(exclude_unset=True)
        updated_place = self._repo.update_place(db=db, place_id=place_id, place_data=place_data)
        if updated_place:
            return updated_place
        else:
            raise ValueError("Place not found")

    def delete_place(self, db: Session, place_id: int):
        # Check if the place has any associated activities
        if db.query(Activity).filter(Activity.place_id == place_id).first():
            raise ValueError("Cannot delete place because it has associated activities")

        # If no associated activities, proceed to delete the place
        self._repo.delete_place(db=db, place_id=place_id)


place_service: PlaceService = PlaceService()
