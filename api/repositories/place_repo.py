from sqlalchemy.orm import Session
from models.place import Place


class PlaceRepo:
    @staticmethod
    def save_place(db: Session, place: Place) -> Place:
        db.add(place)
        db.commit()
        db.refresh(place)
        return place


place_repo: PlaceRepo = PlaceRepo()
