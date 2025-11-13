from .base import Base
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

class BuildingModel(Base):
    __tablename__ = "building"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String)
    street: Mapped[str] = mapped_column(String)
    building_number: Mapped[str] = mapped_column(String)
    apartments: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    @property
    def adress(self):
        return f"г. {self.city}, ул. {self.street} {self.building_number}, {self.apartments}"
    
    @property
    def coordinates(self):
        return [self.latitude, self.longitude]