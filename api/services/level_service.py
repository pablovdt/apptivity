from api.repositories.level_repo import LevelRepo, level_repo
from models.level import Level
from schemas.level_schema import LevelCreate
from sqlalchemy.orm import Session

class LevelService:
    _repo: LevelRepo = level_repo


    def create_level(self, db: Session, level_create: LevelCreate) -> Level:
        level = Level(
            name=level_create.name,
            range_min=level_create.range_min,
            range_max=level_create.range_max
        )
        return self._repo.save_level(db=db, level=level)

level_service: LevelService = LevelService()