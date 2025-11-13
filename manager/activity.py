

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.activity import ActivityModel
from routes.schemas.activity import ActivityCreate


class ActivityManager:
    def __init__(self):
        pass

    def add_activity(self, activity: ActivityCreate, db: Session) -> ActivityModel:

        new_activity = ActivityModel(**activity.model_dump())

        if new_activity.parent_id is not None:
            parent_activity = self.get_by_id(db, new_activity.parent_id)
            if parent_activity is None:
                raise ValueError(f"Parent activity with id {new_activity.parent_id} does not exist.")
            else:
                new_activity.level = parent_activity.level + 1
        if new_activity.level == 3:
            raise ValueError("Activity level cannot be greater than 2.")
        
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)
        return new_activity

    
    def get_all(self, db: Session) -> List[ActivityModel]:
        stmt = select(ActivityModel)
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_by_id(self, db: Session, activity_id: int) -> Optional[ActivityModel]:
        stmt = select(ActivityModel).where(ActivityModel.id == activity_id)
        row = db.execute(stmt).scalar_one_or_none()
        return row
    
    def get_by_name(self, db: Session, name: str) -> Optional[ActivityModel]:
        stmt = select(ActivityModel).where(ActivityModel.name == name)
        row = db.execute(stmt).scalar_one_or_none()
        return row


activity_manager = ActivityManager()