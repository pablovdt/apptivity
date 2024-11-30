from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from api.services.category_service import category_service
from database import get_db
from typing import List, Optional

router = APIRouter()


# Crear nueva categoría
@router.post("/create_category/", response_model=CategoryOut, status_code=201)
def create_category(category_create: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return category_service.create_category(db=db, category_create=category_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Obtener categoría por ID
@router.get("/category/{category_id}/", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    try:
        return category_service.get_category(db=db, category_id=category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Obtener todas las categorías (con filtros opcionales)
@router.get("/categories/", response_model=List[CategoryOut])
def get_all_categories(
        db: Session = Depends(get_db),
        name: Optional[str] = None
):
    filters = {}
    if name:
        filters["name"] = name

    return category_service.get_all_categories(db=db, filters=filters)


# Actualizar categoría por ID
@router.patch("/category/{category_id}/", response_model=CategoryOut)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        return category_service.update_category(db=db, category_id=category_id, category_update=category_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Eliminar categoría por ID
@router.delete("/category/{category_id}/", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category_service.delete_category(db=db, category_id=category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
