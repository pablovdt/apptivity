from sqlalchemy.orm import Session
from models.category import Category

class CategoryRepo:
    @staticmethod
    def save_category(db: Session, category: Category) -> Category:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

category_repo: CategoryRepo = CategoryRepo()
