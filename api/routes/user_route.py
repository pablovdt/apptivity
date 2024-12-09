from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict
from schemas.activity_schema import ActivityOut, ActivityForUserOut
from schemas.organizer_schema import OrganizerForUserOut
from schemas.user_schema import UserCreate, UserUpdate, UserOut, UserActivityFilters, UserMoreActivitiesIn, \
    ValidateQrLocation
from api.services.user_service import user_service
from database import get_db
from typing import List, Optional

router = APIRouter()


@router.post("/create_user/", response_model=UserOut, status_code=201)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db=db, user_create=user_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add_user_activity", status_code=201)
def add_user_activity(user_id: int, activity_id: int, db: Session = Depends(get_db)):
    try:
        user_service.add_user_activity(db=db, user_id=user_id, activity_id=activity_id)
        return f"Actividad  {activity_id} asociada a usuario {user_id}."
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add_user_organizer", status_code=201)
def add_user_organizer(user_id: int, organizer_id: int, db: Session = Depends(get_db)):
    try:
        user_service.add_user_organizer(db=db, user_id=user_id, organizer_id=organizer_id)
        return f"Usuario {user_id} suscrito  a organizador {organizer_id}."
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}/", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_user(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users/", response_model=List[UserOut])
def get_all_users(
        db: Session = Depends(get_db),
        name: Optional[str] = None,
        email: Optional[str] = None,
        category_id: Optional[int] = None
):
    # Construcción de filtros
    filters = {}
    if name:
        filters["name"] = name
    if email:
        filters["email"] = email
    if category_id:
        filters["categories"] = [category_id]  # Filtrar por lista de categorías

    return user_service.get_all_users(db=db, filters=filters)


@router.patch("/user/{user_id}/", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(db=db, user_id=user_id, user_update=user_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/user/{user_id}/", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service.delete_user(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/password_by_email/{email}", response_model=str)
def get_password_by_email(email: str, db: Session = Depends(get_db)):
    try:
        return user_service.get_password_by_email(db=db, email=email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user_by_email/{email}", response_model=UserOut)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    try:
        return user_service.get_user_by_email(db=db, email=email)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}/activities", response_model=List[ActivityForUserOut])
def get_user_activities(user_id: int, filters: UserActivityFilters = Depends(), db: Session = Depends(get_db)):
    try:
        return user_service.get_user_activities(db=db, user_id=user_id, filters=filters)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/more_activities", response_model=List[ActivityForUserOut])
def get_user_more_activities(
        user_id: int,
        categories_ids: List[int] = Query(...),
        db: Session = Depends(get_db)
):
    try:
        user_more_activities = UserMoreActivitiesIn(
            user_id=user_id,
            categories_ids=categories_ids
        )
        return user_service.get_user_more_activities(db=db, user_more_activities=user_more_activities)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{user_id}/organizers", response_model=List[OrganizerForUserOut])
def get_user_organizers(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_user_organizers(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{user_id}/activities_updated", response_model=List[dict])
def get_activities_updated(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_activities_updated(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{user_id}/activities/{activity_id}", response_model=Dict[str, Optional[bool]])
def update_assistance(
        user_id: int,
        activity_id: int,
        possible_assistance: Optional[bool] = Query(default=None),
        db: Session = Depends(get_db)
):
    try:
        return user_service.update_possible_assistance(db=db, user_id=user_id, activity_id=activity_id,
                                                       possible_assistance=possible_assistance)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{user_id}/user_activities/{activity_id}", response_model=Dict[str, Optional[bool]])
def update_activity_updated_confirmed(
        user_id: int,
        activity_id: int,
        updated_confirmed: Optional[bool] = Query(default=None),
        db: Session = Depends(get_db)
):
    try:
        return user_service.update_activity_updated_confirmed(db=db, user_id=user_id, activity_id=activity_id,
                                                       updated_confirmed=updated_confirmed)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/validate_qr_and_location/", response_model=bool, status_code=200)
def validate_qr_and_location(validate_qr_and_location: ValidateQrLocation, db: Session = Depends(get_db)):
    try:
        return user_service.validate_qr_and_location(db=db, validate_qr_and_location=validate_qr_and_location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}/assistances", response_model=int)
def get_assistances(user_id: int, db: Session = Depends(get_db)):
    try:
        return user_service.get_assistances(db=db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))