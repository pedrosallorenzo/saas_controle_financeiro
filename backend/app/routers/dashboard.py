from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db, get_current_user
from app.services import dashboard as dashboard_service

router = APIRouter()


@router.get("/summary")
async def dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await dashboard_service.get_summary(db, current_user.id)


@router.get("/top-categories")
async def top_categories(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await dashboard_service.get_top_categories(db, current_user.id, limit)
