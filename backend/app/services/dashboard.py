from datetime import date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.transaction import Transaction
from app.models.category import Category


async def get_summary(db: AsyncSession, user_id: UUID) -> dict:
    today = date.today()
    first_day = date(today.year, today.month, 1)

    result = await db.execute(
        select(Transaction.type, func.sum(Transaction.amount).label("total"))
        .where(Transaction.user_id == user_id, Transaction.date >= first_day)
        .group_by(Transaction.type)
    )
    rows = result.all()

    receitas = float(next((r.total for r in rows if r.type == "receita"), 0))
    despesas = float(next((r.total for r in rows if r.type == "despesa"), 0))

    return {
        "mes": today.strftime("%Y-%m"),
        "receitas": receitas,
        "despesas": despesas,
        "saldo": receitas - despesas,
    }


async def get_top_categories(db: AsyncSession, user_id: UUID, limit: int = 5) -> list[dict]:
    today = date.today()
    first_day = date(today.year, today.month, 1)

    result = await db.execute(
        select(
            Category.name,
            Category.slug,
            Category.icon,
            func.sum(Transaction.amount).label("total"),
        )
        .join(Category, Transaction.category_id == Category.id)
        .where(
            Transaction.user_id == user_id,
            Transaction.date >= first_day,
            Transaction.type == "despesa",
        )
        .group_by(Category.id, Category.name, Category.slug, Category.icon)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(limit)
    )

    return [
        {"name": r.name, "slug": r.slug, "icon": r.icon, "total": float(r.total)}
        for r in result.all()
    ]
