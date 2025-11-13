from typing import List, Optional

from fastapi import status, Depends, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from database.engine import get_db
from manager.activity import activity_manager
from .schemas.activity import ActivityCreate, ActivityRead


router = APIRouter(
    prefix='/activity', 
    tags=['Виды деятельности']
)


@router.get(
    "/get", 
    response_model=List[ActivityRead], 
    summary="Получить все виды деятельности",
    description="Возвращает полный список всех видов деятельности в системе"
)
async def get_all_activities(
    db: Session = Depends(get_db),
) -> List[ActivityRead]:
    data = activity_manager.get_all(db)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Деятельности не найдены",
        )
    return data


@router.get(
    "/get/by_id/{activity_id}", 
    response_model=ActivityRead, 
    summary="Получить вид деятельности по ID",
    description="Поиск вида деятельности по уникальному идентификатору"
)
async def get_activity_by_id(
    activity_id: int = Path(..., description="Уникальный ID вида деятельности", example=1, ge=1), 
    db: Session = Depends(get_db)
) -> ActivityRead:
    item = activity_manager.get_by_id(db, activity_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Деятельность с id: {activity_id} не найдена",
        )
    return item


@router.get(
    "/get/by_name/{name}", 
    response_model=ActivityRead, 
    summary="Получить вид деятельности по названию",
    description="Поиск вида деятельности по точному названию"
)
async def get_activity_by_name(
    name: str = Path(..., description="Название вида деятельности", example="Еда"), 
    db: Session = Depends(get_db)
) -> ActivityRead:
    item = activity_manager.get_by_name(db, name)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Деятельность с именем: {name} не найдена",
        )
    return item


@router.post(
    "/add", 
    response_model=ActivityRead, 
    status_code=status.HTTP_201_CREATED, 
    summary="Добавить вид деятельности",
    description="Создание нового вида деятельности в системе"
)
async def add_activity(
    activity: ActivityCreate, 
    db: Session = Depends(get_db)
):
    try:
        new_activity = activity_manager.add_activity(activity, db)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(e)}
        )

    return new_activity