from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.place_schema import PlaceCreate, PlaceUpdate, PlaceOut
from api.services.place_service import place_service
from database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/create_place/", response_model=PlaceOut, status_code=201)
def create_place(place_create: PlaceCreate, db: Session = Depends(get_db)):
    try:
        return place_service.create_place(db=db, place_create=place_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/place/{place_id}/", response_model=PlaceOut)
def get_place(place_id: int, db: Session = Depends(get_db)):
    try:
        return place_service.get_place(db=db, place_id=place_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/places/", response_model=List[PlaceOut])
def get_all_places(
    db: Session = Depends(get_db),
    name: Optional[str] = None,
    city_id: Optional[str] = None
):
    filters = {}
    if name:
        filters["name"] = name
    if city_id:
        filters["city_id"] = city_id

    return place_service.get_all_places(db=db, filters=filters)

@router.patch("/place/{place_id}/", response_model=PlaceOut)
def update_place(place_id: int, place_update: PlaceUpdate, db: Session = Depends(get_db)):
    try:
        return place_service.update_place(db=db, place_id=place_id, place_update=place_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/place/{place_id}/", status_code=204)
def delete_place(place_id: int, db: Session = Depends(get_db)):
    try:
        place_service.delete_place(db=db, place_id=place_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
