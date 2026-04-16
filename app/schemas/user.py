"""Pydantic schemas for user-related requests and responses."""
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    monthly_income: float
    monthly_expenses: float
    savings_goal: float
    emergency_fund: float

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = None
    monthly_income: float | None = None
    monthly_expenses: float | None = None
    savings_goal: float | None = None
    emergency_fund: float | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
