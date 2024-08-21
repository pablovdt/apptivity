from sqlalchemy.orm import Session
from models.category import Category
from schemas.category_schema import CategoryCreate, CategoryUpdate
from api.repositories.category_repo import CategoryRepo

class CategoryService:
    _repo: CategoryRepo = CategoryRepo()

    def create_category(self, db: Session, category_create: CategoryCreate) -> Category:
        category = Category(name=category_create.name)
        return self._repo.save_category(db=db, category=category)

    def get_category(self, db: Session, category_id: int) -> Category:
        category = self._repo.get_category_by_id(db=db, category_id=category_id)
        if not category:
            raise ValueError("Categoría no encontrada")
        return category

    def get_all_categories(self, db: Session, filters: dict = None) -> list[Category]:
        return self._repo.get_all_categories(db=db, filters=filters)

    def update_category(self, db: Session, category_id: int, category_update: CategoryUpdate) -> Category:
        category_data = category_update.dict(exclude_unset=True)
        updated_category = self._repo.update_category(db=db, category_id=category_id, category_data=category_data)
        if not updated_category:
            raise ValueError("Categoría no encontrada")
        return updated_category

    def delete_category(self, db: Session, category_id: int):
        self._repo.delete_category(db=db, category_id=category_id)
