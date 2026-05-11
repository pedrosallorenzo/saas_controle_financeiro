import uuid
from sqlalchemy import (
    CheckConstraint, Column, Date, DateTime, ForeignKey, Index, Numeric, Text, func,
)
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    type = Column(Text, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    description = Column(Text)
    date = Column(Date, nullable=False)
    raw_input = Column(Text)
    ai_confidence = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("type IN ('receita', 'despesa')", name="ck_transactions_type"),
        CheckConstraint("amount > 0", name="ck_transactions_amount_positive"),
        CheckConstraint(
            "ai_confidence IN ('alta', 'media', 'baixa')",
            name="ck_transactions_ai_confidence",
        ),
        Index("idx_transactions_user_date", "user_id", "date"),
        Index("idx_transactions_user_type", "user_id", "type"),
    )
