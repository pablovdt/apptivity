from sqlalchemy.orm import Session

from models.level import Level



class LevelRepo:
    @staticmethod
    def save_level(db: Session, level: Level) -> Level:
        db.add(level)
        db.commit()
        db.refresh(level)
        return level

    @staticmethod
    def get_level_id(db: Session, level_name: str):
        result = db.query(Level.id).filter(Level.name == level_name).first()
        return result[0] if result else None

level_repo: LevelRepo = LevelRepo()
