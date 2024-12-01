from sqlalchemy.orm import Session
from models.city import City
from schemas.city_schema import CityCreate, CityUpdate
from api.repositories.city_repo import CityRepo

class CityService:
    _repo: CityRepo = CityRepo()

    def create_city(self, db: Session, city_create: CityCreate) -> City:
        city = City(
            cp=city_create.cp,  # Suponiendo que 'cp' es proporcionado en la creación
            name=city_create.name,
            latitude=city_create.latitude,
            longitude=city_create.longitude
        )
        return self._repo.save_city(db=db, city=city)

    def get_city_by_cp(self, db: Session, city_cp: str) -> City:
        city = self._repo.get_city_by_cp(db=db, city_cp=city_cp)
        if not city:
            raise ValueError("Ciudad no encontrada")
        return city

    def get_city_by_id(self, db: Session, city_id: int) -> City:
        city = self._repo.get_city_by_id(db=db, city_id=city_id)
        if not city:
            raise ValueError("Ciudad no encontrada")
        return city

    def get_all_cities(self, db: Session, filters: dict = None) -> list[City]:
        return self._repo.get_all_cities(db=db, filters=filters)

    def update_city(self, db: Session, city_cp: str, city_update: CityUpdate) -> City:
        city_data = city_update.dict(exclude_unset=True)
        updated_city = self._repo.update_city(db=db, city_cp=city_cp, city_data=city_data)
        if not updated_city:
            raise ValueError("Ciudad no encontrada")
        return updated_city

    def delete_city(self, db: Session, city_cp: str):
        try:
            self._repo.delete_city(db=db, city_cp=city_cp)
        except ValueError as e:
            raise ValueError(str(e))
