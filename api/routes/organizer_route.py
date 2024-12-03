from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.organizer_schema import OrganizerCreate, OrganizerUpdate, OrganizerOut
from api.services.organizer_service import organizer_service
from database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/create_organizer/", response_model=OrganizerOut, status_code=201)
def create_organizer(organizer_create: OrganizerCreate, db: Session = Depends(get_db)):
    try:
        return organizer_service.create_organizer(db=db, organizer_create=organizer_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/organizer/{organizer_id}/", response_model=OrganizerOut)
def get_organizer(organizer_id: int, db: Session = Depends(get_db)):
    try:
        return organizer_service.get_organizer(db=db, organizer_id=organizer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/organizers/", response_model=List[OrganizerOut])
def get_all_organizers(
    db: Session = Depends(get_db),
    name: Optional[str] = None,
    city_cp: Optional[str] = None
):
    filters = {}
    if name:
        filters["name"] = name
    if city_cp:
        filters["city_cp"] = city_cp

    return organizer_service.get_all_organizers(db=db, filters=filters)

@router.patch("/organizer/{organizer_id}/", response_model=OrganizerOut)
def update_organizer(organizer_id: int, organizer_update: OrganizerUpdate, db: Session = Depends(get_db)):
    try:
        # Añadido para permitir la actualización del campo password
        return organizer_service.update_organizer(db=db, organizer_id=organizer_id, organizer_update=organizer_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/organizer/{organizer_id}/", status_code=204)
def delete_organizer(organizer_id: int, db: Session = Depends(get_db)):
    try:
        organizer_service.delete_organizer(db=db, organizer_id=organizer_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/organizer/password_by_email/{email}", response_model=str)
def get_password_by_email(email: str, db: Session = Depends(get_db)):
    try:
        return organizer_service.get_password_by_email(db=db, email=email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/organizer_by_email/{email}", response_model=OrganizerOut)
def get_organizer_by_email(email: str, db: Session = Depends(get_db)):
    try:
        return organizer_service.get_organizer_by_email(db=db, email=email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user_coordinates/{organizer_id}", response_model=list[dict])
def get_coordinates_from_users(organizer_id: int, db: Session = Depends(get_db)):
    try:
        return organizer_service.get_coordinates_from_users(db=db, organizer_id=organizer_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
