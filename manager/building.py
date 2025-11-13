from typing import List, Tuple
import math

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.building import BuildingModel
from routes.schemas.building import BuildingCreate

from utils.point_in_radius import is_point_in_radius

class BuildingManager:
    def __init__(self):
        pass
    
    def add_building(self, building: BuildingCreate, db: Session) -> BuildingModel:
        new_building = BuildingModel(**building.model_dump())
        print(new_building.adress)
        if db.query(BuildingModel).filter(BuildingModel.adress == new_building.adress).first():
            raise ValueError(f"Здание с адресом {new_building.adress} уже существует.")
        db.add(new_building)
        db.commit()
        return new_building

    def get_all(self, db: Session) -> List[BuildingModel]:
        stmt = select(BuildingModel)
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_by_id(self, db: Session, building_id: int) -> BuildingModel:
        stmt = select(BuildingModel).where(BuildingModel.id == building_id)
        row = db.execute(stmt).scalar_one_or_none()
        return row
    
    def get_by_lat_lon(self, db: Session, latitude: float, longitude: float) -> BuildingModel:
        stmt = select(BuildingModel).where(
            BuildingModel.latitude == latitude,
            BuildingModel.longitude == longitude
        )
        row = db.execute(stmt).scalar_one_or_none()
        return row
    
    def get_by_rectangle(self, db: Session, 
                         lat_min: float, lat_max: float,
                         lon_min: float, lon_max: float) -> List[BuildingModel]:
        stmt = select(BuildingModel).where(
            BuildingModel.latitude.between(lat_min, lat_max),
            BuildingModel.longitude.between(lon_min, lon_max)
        )
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_by_radius(self, db: Session, center_lat: float, center_lon: float, radius_m: float) -> List[Tuple[BuildingModel, float]]:
        lat_offset, lon_offset = self.calculate_degree_offsets(center_lat, radius_m)
    
        lat_min = center_lat - lat_offset
        lat_max = center_lat + lat_offset
        lon_min = center_lon - lon_offset
        lon_max = center_lon + lon_offset
        
        buildings = self.get_by_rectangle(db, lat_min, lat_max, lon_min, lon_max)

        buildings_in_radius = []
        
        for building in buildings:
            if is_point_in_radius([building.latitude, building.longitude], [center_lat, center_lon], radius_m):
                buildings_in_radius.append(building.id)
        return buildings_in_radius      

    def calculate_degree_offsets(self, latitude: float, radius_m: float, margin: float = 1.1) -> tuple[float, float]:
        METERS_PER_DEGREE_LAT = 111320 
        METERS_PER_DEGREE_LON = 111320 * math.cos(math.radians(latitude))
        
        lat_offset = (radius_m * margin) / METERS_PER_DEGREE_LAT
        lon_offset = (radius_m * margin) / METERS_PER_DEGREE_LON
        
        return lat_offset, lon_offset      


building_manager = BuildingManager()