from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.place_schema import PlaceCreate, PlaceOut
from api.services.place_service import place_service
from database import get_db

router = APIRouter()

@router.post("/create_place/", response_model=PlaceOut, status_code=201)
def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    try:
        created_place = place_service.create_place(db=db, place_create=place)
        return created_place
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear el lugar")
