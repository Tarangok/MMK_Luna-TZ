from typing import List

from fastapi import status, Depends, HTTPException, Query, Path
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from database.engine import get_db
from manager.organization import organization_manager
from .schemas.organization import OrganizationCreate, OrganizationRead


router = APIRouter(
    prefix='/organization', 
    tags=['Организации']
)


@router.get(
    "/get_all", 
    response_model=List[OrganizationRead], 
    summary="Получить все организации",
    description="Возвращает полный список всех организаций системы"
)
async def get_all_organizations(
    db: Session = Depends(get_db)
) -> List[OrganizationRead]:
    data = organization_manager.get_all(db)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организации не найдены",
        )
    return data


@router.get(
    "/get/by_id/{org_id}", 
    response_model=OrganizationRead, 
    summary="Получить организацию по ID",
    description="Поиск организации по уникальному идентификатору"
)
async def get_organization_by_id(
    org_id: int = Path(..., description="Уникальный ID организации", example=1, ge=1), 
    db: Session = Depends(get_db)
) -> OrganizationRead:
    item = organization_manager.get_by_id(db, org_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организация с id: {org_id} не найдена",
        )
    return item


@router.get(
    "/get/by_name/{name}", 
    response_model=OrganizationRead, 
    summary="Поиск по названию",
    description="Поиск организации по точному названию"
)
async def get_organization_by_name(
    name: str = Path(..., description="Название организации", example="ООО Ромашка"), 
    db: Session = Depends(get_db)
) -> OrganizationRead:
    item = organization_manager.get_by_name(db, name)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организация с именем: {name} не найдена",
        )
    return item


@router.get(
    "/get/by_building_id/{building_id}", 
    response_model=List[OrganizationRead], 
    summary="Организации в здании",
    description="Получить все организации в указанном здании"
)
async def get_organizations_by_building(
    building_id: int = Path(..., description="ID здания", example=1, ge=1), 
    db: Session = Depends(get_db)
) -> List[OrganizationRead]:
    data = organization_manager.get_all_by_building(db, building_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организации в здании с id: {building_id} не найдены",
        )
    return data


@router.get(
    "/get/by_activity_id/{activity_id}", 
    response_model=List[OrganizationRead], 
    summary="Организации по виду деятельности",
    description="Поиск организаций по виду деятельности"
)
async def get_organizations_by_activity(
    activity_id: int = Path(..., description="ID вида деятельности", example=1, ge=1), 
    db: Session = Depends(get_db)
) -> List[OrganizationRead]:
    data = organization_manager.get_all_by_activity(db, activity_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Организации по деятельности с id: {activity_id} не найдены",
        )
    return data


@router.get(
    "/get/by_radius/", 
    response_model=List[OrganizationRead], 
    summary="Поиск в радиусе",
    description="Геопоиск организаций в радиусе от точки"
)
async def get_organizations_by_radius(
    center_lat: float = Query(..., description="Широта центра (°)", example=55.7558, ge=-90, le=90),
    center_lon: float = Query(..., description="Долгота центра (°)", example=37.6173, ge=-180, le=180),
    radius_m: float = Query(..., description="Радиус поиска (метры)", example=1000, ge=0),
    db: Session = Depends(get_db)
) -> List[OrganizationRead]:
    data = organization_manager.get_organization_in_radius(db, center_lat, center_lon, radius_m)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организации в радиусе не найдены",
        )
    return data


@router.get(
    "/get/by_rectangle/", 
    response_model=List[OrganizationRead], 
    summary="Поиск в прямоугольнике", 
    description="**Геопоиск организаций в прямоугольной области**"
)
async def get_organizations_by_rectangle(
    lat_min: float = Query(..., description="Минимальная широта (°)", example=55.0),
    lat_max: float = Query(..., description="Максимальная широта (°)", example=56.0),
    lon_min: float = Query(..., description="Минимальная долгота (°)", example=37.0),
    lon_max: float = Query(..., description="Максимальная долгота (°)", example=38.0),
    db: Session = Depends(get_db)
) -> List[OrganizationRead]:
    data = organization_manager.get_organization_in_rectangle(db, lat_min, lat_max, lon_min, lon_max)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Организации в прямоугольнике не найдены",
        )
    return data


@router.post(
    "/add", 
    response_model=OrganizationRead, 
    status_code=status.HTTP_201_CREATED, 
    summary="Добавить организацию",
    description="Создание новой организации в системе",
)
async def add_organization(
    organization: OrganizationCreate, 
    db: Session = Depends(get_db)
):
    new_organization = organization_manager.add_organization(organization, db)
    return new_organization