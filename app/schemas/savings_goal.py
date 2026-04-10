from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class SavingsGoalCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    target_amount: float = Field(..., gt=0)
    auto_save_rule: Optional[dict] = None
    deadline: Optional[date] = None
    emoji: str = "🎯"


class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    target_amount: Optional[float] = Field(None, gt=0)
    auto_save_rule: Optional[dict] = None
    deadline: Optional[date] = None
    emoji: Optional[str] = None


class ContributeRequest(BaseModel):
    amount: float = Field(..., gt=0)


class SavingsGoalResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: str
    user_id: str
    name: str
    target_amount: float
    current_amount: float
    auto_save_rule: Optional[dict] = None
    deadline: Optional[date] = None
    emoji: str
    progress_pct: float = 0.0
    created_at: datetime
