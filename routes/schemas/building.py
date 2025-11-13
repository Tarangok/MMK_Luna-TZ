from typing import Optional

from pydantic import BaseModel


class BuildingCreate(BaseModel):
    city: str
    street: str
    building_number: str
    apartments: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True


class BuildingRead(BaseModel):
    id: int
    city: str
    street: str
    building_number: str
    apartments: str
    latitude: float
    longitude: float
    adress: str
    coordinates: list[float, float]

    class Config:
        from_attributes = True
