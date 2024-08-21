from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.activity_schema import ActivityOut, ActivityUpdate, ActivityCreate, ActivityFilters
from api.services.activity_service import activity_service
from database import get_db
from typing import Optional, List

router = APIRouter()


# Crear nueva actividad
@router.post("/create_activity/", response_model=ActivityOut, status_code=201)
def create_activity(activity_create: ActivityCreate, db: Session = Depends(get_db)):
    try:
        created_activity = activity_service.create_activity(db=db, activity_create=activity_create)
        return created_activity
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Obtener actividad por ID
@router.get("/activity/{activity_id}/", response_model=ActivityOut)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    try:
        return activity_service.get_activity(db=db, activity_id=activity_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Obtener todas las actividades (con filtros opcionales)
@router.get("/activities/", response_model=List[ActivityOut])
def get_all_activities(filters: ActivityFilters = Depends(), db: Session = Depends(get_db)):
    try:
        return activity_service.get_all_activities(db=db, filters=filters)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Actualizar actividad por ID
@router.patch("/activity/{activity_id}/", response_model=ActivityOut)
def update_activity(activity_id: int, activity_update: ActivityUpdate, db: Session = Depends(get_db)):
    try:
        return activity_service.update_activity(db=db, activity_id=activity_id, activity_update=activity_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Eliminar actividad por ID
@router.delete("/activity/{activity_id}/", status_code=204)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    try:
        activity_service.delete_activity(db=db, activity_id=activity_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
