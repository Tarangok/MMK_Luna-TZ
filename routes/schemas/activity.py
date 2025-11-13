from typing import Optional

from pydantic import BaseModel


class ActivityCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class ActivityRead(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    level: int = 0

    class Config:
        from_attributes = True
