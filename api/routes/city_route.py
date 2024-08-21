from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.city_schema import CityCreate, CityOut
from api.services.city_service import city_service
from database import get_db

router = APIRouter()

@router.post("/create_city/", response_model=CityOut, status_code=201)
def create_new_city(city: CityCreate, db: Session = Depends(get_db)):
    try:
        created_city = city_service.create_city(db=db, city_create=city)
        return created_city
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
