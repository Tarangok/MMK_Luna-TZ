from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from database.models.organization import OrganizationModel
from database.models.activity import ActivityModel
from database.models.organization_activities import OrganizationActivityModel
from routes.schemas.organization import OrganizationCreate

from .organization_activities import organization_activity_manager
from .building import building_manager


class OrganizationManager:
    def __init__(self):
        pass

    def add_organization(self, organization: OrganizationCreate, db: Session) -> OrganizationModel:
        new_organization = OrganizationModel(**organization.model_dump(exclude={"activity_ids"}))
        for activity_id in organization.activity_ids:
            activity = db.get(ActivityModel, activity_id)
            if activity:
                organization_activity_manager.add_activity_to_organization(db, new_organization, activity)
        db.add(new_organization)
        db.commit()
        db.refresh(new_organization)
        return new_organization

    def get_all(self, db: Session) -> List[OrganizationModel]:
        stmt = select(OrganizationModel)
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_by_id(self, db: Session, organization_id: int) -> OrganizationModel:
        stmt = select(OrganizationModel).where(OrganizationModel.id == organization_id)
        row = db.execute(stmt).scalar_one_or_none()
        return row
    
    def get_by_name(self, db: Session, name: str) -> OrganizationModel:
        stmt = select(OrganizationModel).where(OrganizationModel.name == name)
        row = db.execute(stmt).scalar_one_or_none()
        return row
    
    def get_all_by_building(self, db: Session, building_id: int) -> List[OrganizationModel]:
        stmt = select(OrganizationModel).where(OrganizationModel.building_id == building_id)
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_all_by_activity(self, db: Session, activity_id: int) -> List[OrganizationModel]:
        activity_cte = (
            select(ActivityModel.id)
            .where(ActivityModel.id == activity_id)
            .cte(name="activity_tree", recursive=True)
        )
        
        activity_alias = aliased(ActivityModel, name="a")
        recursive = (
            select(activity_alias.id)
            .where(activity_alias.parent_id == activity_cte.c.id)
        )
        activity_cte = activity_cte.union_all(recursive)

        stmt = (
            select(OrganizationModel)
            .distinct(OrganizationModel.id)
            .join(OrganizationModel.activity_associations)
            .join(OrganizationActivityModel.activity)
            .where(ActivityModel.id.in_(select(activity_cte.c.id)))
        )
        
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_organization_activities(self, db: Session, organization_id: int) -> List[ActivityModel]:
        stmt = (
            select(ActivityModel)
            .join(OrganizationActivityModel.activity)
            .where(OrganizationActivityModel.organization_id == organization_id)
        )
    
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_organization_in_rectangle(self, db: Session,
                                  lat_min: float, lat_max: float,
                                  lon_min: float, lon_max: float) -> List[OrganizationModel]:
        buildings = building_manager.get_by_rectangle(db, lat_min, lat_max, lon_min, lon_max)
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.building_id.in_([building.id for building in buildings]))
        )
        rows = db.execute(stmt).scalars().all()
        return rows
    
    def get_organization_in_radius(self, db: Session,
                                 center_lat: float, center_lon: float,
                                 radius_m: float) -> List[OrganizationModel]:
        building_ids = building_manager.get_by_radius(db, center_lat, center_lon, radius_m)
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.building_id.in_(building_ids))
        )
        rows = db.execute(stmt).scalars().all()
        return rows
        

organization_manager = OrganizationManager()