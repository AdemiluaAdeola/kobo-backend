"""Pydantic schemas for transactions."""
from datetime import datetime

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: float
    description: str
    transaction_type: str = "debit"  # debit / credit
    transaction_date: datetime | None = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    category: str | None
    confidence_score: float | None
    transaction_type: str
    transaction_date: datetime
    created_at: datetime

    model_config = {"from_attributes": True}
