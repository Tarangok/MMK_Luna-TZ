from typing import List, Optional

from fastapi import HTTPException, status, Depends, Query, Path
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from database.engine import get_db
from manager.building import building_manager
from .schemas.building import BuildingRead, BuildingCreate


router = APIRouter(
    prefix='/building', 
    tags=['Здания']
)


@router.get(
    "/get_all", 
    response_model=List[BuildingRead], 
    summary="Получить все здания",
    description="Возвращает полный список всех зданий, зарегистрированных в системе."
)
async def get_all_buildings(
    db: Session = Depends(get_db)
) -> List[BuildingRead]:
    data = building_manager.get_all(db)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здания не найдены",
        )
    return data


@router.get(
    "/get/by_id/{building_id}", 
    response_model=BuildingRead, 
    summary="Получить здание по ID",
    description="Поиск здания по уникальному идентификатору"
)
async def get_organization_by_id(
    building_id: int = Path(..., description="Уникальный ID здания", example=1, ge=1), 
    db: Session = Depends(get_db)
) -> BuildingRead:
    item = building_manager.get_by_id(db, building_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Здание с id: {building_id} не найдена",
        )
    return item


@router.post(
    "/add", 
    response_model=BuildingRead, 
    status_code=status.HTTP_201_CREATED, 
    summary="Добавить здание",
    description="Создание нового здания в системе"
)
async def add_building(
    building: BuildingCreate, 
    db: Session = Depends(get_db)
):
    new_building = building_manager.add_building(building, db)
    return new_building