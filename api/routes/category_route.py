from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.category_schema import CategoryCreate, CategoryOut
from api.services.category_service import category_service
from database import get_db

router = APIRouter()

@router.post("/create_category/", response_model=CategoryOut, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        created_category = category_service.create_category(db=db, category_create=category)
        return created_category
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al crear la categoría")
