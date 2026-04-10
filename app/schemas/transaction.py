from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class TransactionCreate(BaseModel):
    type: str = Field(..., pattern="^(income|expenditure)$")
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=80)
    description: str = ""
    date: Optional[date] = None
    source: str = "manual"
    is_recurring: bool = False


class TransactionUpdate(BaseModel):
    type: Optional[str] = Field(None, pattern="^(income|expenditure)$")
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=80)
    description: Optional[str] = None
    date: Optional[date] = None
    is_recurring: Optional[bool] = None


class TransactionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    type: str
    amount: float
    category: str
    description: str
    date: date
    source: str
    is_recurring: bool
    created_at: datetime
