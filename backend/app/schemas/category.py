from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None


class CategoryOut(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    slug: str
    icon: Optional[str]
    is_default: bool

    model_config = {"from_attributes": True}
