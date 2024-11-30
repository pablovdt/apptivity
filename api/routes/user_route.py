from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserUpdate, UserOut
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

    # Obtener usuarios según los filtros
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
