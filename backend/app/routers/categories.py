from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.deps import get_db, get_current_user
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter()


@router.get("", response_model=list[CategoryOut])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(
        select(Category).where(Category.user_id == current_user.id)
    )
    return result.scalars().all()


@router.post("", response_model=CategoryOut, status_code=201)
async def create_category(
    body: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    category = Category(**body.model_dump(), user_id=current_user.id)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category
