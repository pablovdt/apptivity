from sqlalchemy.orm import Session

from models import Place
from models.city import City
from models.activity import Activity  # Asegúrate de importar esto para comprobar actividades

class CityRepo:

    @staticmethod
    def save_city(db: Session, city: City) -> City:
        db.add(city)
        db.commit()
        db.refresh(city)
        return city

    @staticmethod
    def get_city_by_cp(db: Session, city_cp: str) -> City:
        return db.query(City).filter(City.cp == city_cp).first()

    @staticmethod
    def get_city_by_id(db: Session, city_id: int) -> City:
        return db.query(City).filter(City.id == city_id).first()

    @staticmethod
    def get_all_cities(db: Session, filters: dict = None) -> list[City]:
        query = db.query(City)

        if filters:
            for key, value in filters.items():
                if key == "name" and value:
                    query = query.filter(City.name.ilike(f"%{value}%"))  # Filtro "contains"
                else:
                    query = query.filter(getattr(City, key) == value)

        return query.all()

    @staticmethod
    def update_city(db: Session, city_cp: str, city_data: dict) -> City:
        city = db.query(City).filter(City.cp == city_cp).first()
        if not city:
            return None
        for key, value in city_data.items():
            setattr(city, key, value)
        db.commit()
        db.refresh(city)
        return city

    @staticmethod
    def delete_city(db: Session, city_cp: str):
        # Comprobar si hay lugares asociados a la ciudad
        if db.query(Activity).filter(Activity.place_id.in_(db.query(Place.id).filter(Place.city_id == city_cp))).first():
            raise ValueError("No se puede eliminar la ciudad porque tiene actividades asociadas a lugares en esta ciudad")

        city = db.query(City).filter(City.cp == city_cp).first()
        if city:
            db.delete(city)
            db.commit()
        else:
            raise ValueError("Ciudad no encontrada")
