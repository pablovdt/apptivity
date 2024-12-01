from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.city_schema import CityCreate, CityUpdate, CityOut
from api.services.city_service import CityService
from database import get_db
from typing import List, Optional

router = APIRouter()

city_service = CityService()

@router.post("/create_city/", response_model=CityOut, status_code=201)
def create_city(city_create: CityCreate, db: Session = Depends(get_db)):
    try:
        return city_service.create_city(db=db, city_create=city_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/city/{city_cp}/", response_model=CityOut)
def get_city(city_cp: str, db: Session = Depends(get_db)):
    try:
        return city_service.get_city_by_cp(db=db, city_cp=city_cp)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/city/id/{city_id}/", response_model=CityOut)
def get_city(city_id: int, db: Session = Depends(get_db)):
    try:
        return city_service.get_city_by_id(db=db, city_id=city_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/cities/", response_model=List[CityOut])
def get_all_cities(
    db: Session = Depends(get_db),
    name: Optional[str] = None
):
    filters = {}
    if name:
        filters["name"] = name

    return city_service.get_all_cities(db=db, filters=filters)

@router.put("/city/{city_cp}/", response_model=CityOut)
def update_city(city_cp: str, city_update: CityUpdate, db: Session = Depends(get_db)):
    try:
        return city_service.update_city(db=db, city_cp=city_cp, city_update=city_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/city/{city_cp}/", status_code=204)
def delete_city(city_cp: str, db: Session = Depends(get_db)):
    try:
        city_service.delete_city(db=db, city_cp=city_cp)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
