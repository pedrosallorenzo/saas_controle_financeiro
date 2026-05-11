from datetime import date
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, field_validator


class TransactionCreate(BaseModel):
    category_id: Optional[UUID] = None
    type: str
    amount: Decimal
    description: Optional[str] = None
    date: date
    raw_input: Optional[str] = None
    ai_confidence: Optional[str] = None

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if v not in ("receita", "despesa"):
            raise ValueError("type deve ser 'receita' ou 'despesa'")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount deve ser positivo")
        return v


class TransactionUpdate(BaseModel):
    category_id: Optional[UUID] = None
    type: Optional[str] = None
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    date: Optional[date] = None


class TransactionOut(BaseModel):
    id: UUID
    user_id: UUID
    category_id: Optional[UUID]
    type: str
    amount: Decimal
    description: Optional[str]
    date: date
    raw_input: Optional[str]
    ai_confidence: Optional[str]

    model_config = {"from_attributes": True}
