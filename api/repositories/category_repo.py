from sqlalchemy.orm import Session

from models import Activity
from models.category import Category

class CategoryRepo:

    @staticmethod
    def save_category(db: Session, category: Category) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Category:
        return db.query(Category).filter(Category.id == category_id).first()

    @staticmethod
    def get_all_categories(db: Session, filters: dict = None) -> list[Category]:
        query = db.query(Category)

        if filters:
            for key, value in filters.items():
                if key == "name" and value:
                    query = query.filter(Category.name.ilike(f"%{value}%"))  # Filtro "contains"
                else:
                    query = query.filter(getattr(Category, key) == value)

        return query.all()

    @staticmethod
    def update_category(db: Session, category_id: int, category_data: dict) -> Category:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return None
        for key, value in category_data.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category(db: Session, category_id: int):
        # Comprobar si hay actividades asociadas
        if db.query(Activity).filter(Activity.category_id == category_id).first():
            raise ValueError("No se puede eliminar la categoría porque tiene actividades asociadas")

        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            db.delete(category)
            db.commit()
        else:
            raise ValueError("Categoría no encontrada")
