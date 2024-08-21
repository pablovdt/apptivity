from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserOut
from api.services.user_service import user_service
from database import get_db

router = APIRouter()


@router.post("/create_user/", response_model=UserOut, status_code=201)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        created_user = user_service.create_user(db=db, user_create=user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear el usuario")
