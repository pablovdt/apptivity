from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.organizer_schema import OrganizerCreate, OrganizerOut
from api.services.organizer_service import organizer_service
from database import get_db

router = APIRouter()

@router.post("/create_organizer/", response_model=OrganizerOut, status_code=201)
def create_organizer(organizer: OrganizerCreate, db: Session = Depends(get_db)):
    try:
        created_organizer = organizer_service.create_organizer(db=db, organizer_create=organizer)
        return created_organizer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear el organizador")
