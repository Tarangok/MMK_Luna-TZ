from .base import Base
from sqlalchemy import String, ForeignKey, Integer
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship


class ActivityModel(Base):
    __tablename__ = "activity"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("activity.id"), nullable=True)
    parent_activity: Mapped[Optional["ActivityModel"]] = relationship(
        "ActivityModel",
        remote_side=[id],
        backref="children",
        foreign_keys=[parent_id],
    )
    level: Mapped[int] = mapped_column(Integer, default=0)
    