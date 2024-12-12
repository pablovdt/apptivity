from sqlalchemy.orm import Session

from models.level import Level



class LevelRepo:
    @staticmethod
    def save_level(db: Session, level: Level) -> Level:
        db.add(level)
        db.commit()
        db.refresh(level)
        return level


level_repo: LevelRepo = LevelRepo()
