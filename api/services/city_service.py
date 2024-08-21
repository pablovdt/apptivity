from sqlalchemy.orm import Session
from models.city import City
from schemas.city_schema import CityCreate
from api.repositories.city_repo import city_repo, CityRepo


class CityService:
    _repo: CityRepo = city_repo

    def create_city(self, db: Session, city_create: CityCreate) -> City:
        if db.query(City).filter(City.cp == city_create.cp).first():
            raise ValueError("El código postal ya está registrado")

        city = City(
            cp=city_create.cp,
            name=city_create.name,
            latitude=city_create.latitude,
            longitude=city_create.longitude
        )

        return self._repo.save_city(db=db, city=city)


city_service: CityService = CityService()
