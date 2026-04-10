from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class ForecastPoint(BaseModel):
    date: date
    predicted_balance: float
    label: str  # e.g. "Today", "Day 3"


class CashFlowSummary(BaseModel):
    total_income: float
    total_expenditure: float
    net: float
    top_categories: List[dict]  # [{"category": "food", "amount": 45000}, ...]


class NetWorthResponse(BaseModel):
    total_assets: float
    total_liabilities: float
    net_worth: float
    assets_breakdown: List[dict]   # [{"type": "stocks", "value": 2100000}, ...]
    debts_breakdown: List[dict]    # [{"name": "Palmcredit", "amount": 150000}, ...]
    monthly_income: float
    monthly_expenditure: float
