from typing import List

from pydantic import BaseModel

from .building import BuildingRead
from .activity import ActivityRead


class OrganizationCreate(BaseModel):
    name: str
    phone: List[str]
    building_id: int
    activity_ids: List[int]

    class Config:
        from_attributes = True


class OrganizationRead(BaseModel):
    id: int
    name: str
    phone: List[str]
    building: BuildingRead
    activities: List[ActivityRead]

    class Config:
        from_attributes = True
