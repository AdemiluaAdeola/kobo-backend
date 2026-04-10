from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BudgetCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=80)
    limit_amount: float = Field(..., gt=0)
    period: str = Field("monthly", pattern="^(weekly|monthly)$")


class BudgetUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=80)
    limit_amount: Optional[float] = Field(None, gt=0)
    period: Optional[str] = Field(None, pattern="^(weekly|monthly)$")
    is_frozen: Optional[bool] = None


class BudgetResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    category: str
    limit_amount: float
    period: str
    is_frozen: bool
    created_at: datetime
