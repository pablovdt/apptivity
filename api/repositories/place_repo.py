from sqlalchemy.orm import Session
from models.place import Place

class PlaceRepo:
    @staticmethod
    def save_place(db: Session, place: Place) -> Place:
        db.add(place)
        db.commit()
        db.refresh(place)
        return place

    @staticmethod
    def get_place(db: Session, place_id: int) -> Place:
        return db.query(Place).filter(Place.id == place_id).first()

    @staticmethod
    def get_all_places(db: Session, filters: dict = None) -> list[Place]:
        query = db.query(Place)
        if filters:
            for key, value in filters.items():
                if key in ["name"]:
                    query = query.filter(getattr(Place, key).ilike(f"%{value}%"))
                else:
                    query = query.filter(getattr(Place, key) == value)
        return query.all()

    @staticmethod
    def update_place(db: Session, place_id: int, place_data: dict) -> Place:
        place = db.query(Place).filter(Place.id == place_id).first()
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)
            db.commit()
            db.refresh(place)
            return place
        else:
            return None

    @staticmethod
    def delete_place(db: Session, place_id: int):
        place = db.query(Place).filter(Place.id == place_id).first()
        if place:
            db.delete(place)
            db.commit()
        else:
            raise ValueError("Place not found")

place_repo: PlaceRepo = PlaceRepo()
