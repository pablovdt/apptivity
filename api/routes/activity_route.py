from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.activity_schema import ActivityCreate, ActivityOut
from api.services.activity_service import activity_service
from database import get_db

router = APIRouter()

@router.post("/create_activity/", response_model=ActivityOut, status_code=201)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    try:
        created_activity = activity_service.create_activity(db=db, activity_create=activity)
        return created_activity
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear la actividad")
