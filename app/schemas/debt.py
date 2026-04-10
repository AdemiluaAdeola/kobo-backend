from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class DebtCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    type: str = Field(..., pattern="^(formal|informal)$")
    amount: float = Field(..., gt=0)
    interest_rate: float = Field(0.0, ge=0)
    due_date: Optional[date] = None
    creditor: str = ""
    notes: str = ""


class DebtUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    amount: Optional[float] = Field(None, gt=0)
    interest_rate: Optional[float] = Field(None, ge=0)
    due_date: Optional[date] = None
    creditor: Optional[str] = None
    notes: Optional[str] = None
    is_paid: Optional[bool] = None


class DebtResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    name: str
    type: str
    amount: float
    interest_rate: float
    due_date: Optional[date] = None
    creditor: str
    notes: str
    is_paid: bool
    created_at: datetime
