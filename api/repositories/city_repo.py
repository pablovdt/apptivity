from sqlalchemy.orm import Session
from models.city import City


class CityRepo:
    @staticmethod
    def save_city(db: Session, city: City) -> City:
        db.add(city)
        db.commit()
        db.refresh(city)
        return city


city_repo: CityRepo = CityRepo()
