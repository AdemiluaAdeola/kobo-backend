"""Pydantic schemas for the 14-day cash flow forecast."""
from datetime import date

from pydantic import BaseModel


class ForecastDay(BaseModel):
    date: date
    predicted_balance: float
    predicted_income: float
    predicted_expense: float
    confidence: float


class ForecastResponse(BaseModel):
    forecast: list[ForecastDay]
    current_balance: float
    safe_to_spend: float
    risk_alert: str | None = None
