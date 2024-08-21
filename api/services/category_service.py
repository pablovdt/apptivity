from sqlalchemy.orm import Session
from models.category import Category
from schemas.category_schema import CategoryCreate
from api.repositories.category_repo import category_repo, CategoryRepo


class CategoryService:
    _repo: CategoryRepo = category_repo

    def create_category(self, db: Session, category_create: CategoryCreate) -> Category:
        # Aquí podrías añadir validaciones adicionales si es necesario
        category = Category(
            name=category_create.name,
        )

        return self._repo.save_category(db=db, category=category)

category_service: CategoryService = CategoryService()
