from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class OrganizationActivityModel(Base):
    __tablename__ = "organization_activity"
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["OrganizationModel"] = relationship(
        "OrganizationModel", 
        backref="activity_associations"
    )
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id"))
    activity: Mapped["ActivityModel"] = relationship(
        "ActivityModel", 
        backref="organization_associations"
    )