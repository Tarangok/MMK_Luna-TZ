from typing import Optional

from .base import Base
from sqlalchemy import String, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .organization_activities import OrganizationActivityModel

class OrganizationModel(Base):
    __tablename__ = "organization"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[list] = mapped_column(ARRAY(String))
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    building: Mapped[Optional["BuildingModel"]] = relationship(
        "BuildingModel",
        backref="organizations",
        foreign_keys=[building_id],
    )
    @property
    def activities(self):
        return [assoc.activity for assoc in self.activity_associations]
    
    def add_activity(self, activity):
        assoc = OrganizationActivityModel(activity=activity)
        self.activity_associations.append(assoc)

