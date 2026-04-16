"""
Stub forecast service — returns sample 14-day forecast data.
In production, this would use Facebook Prophet to build forecasts
from the user's transaction history.
"""
from datetime import date, timedelta
import math
import random


def generate_forecast(
    current_balance: float = 156_200.0,
    monthly_income: float = 0.0,
    monthly_expenses: float = 0.0,
    days: int = 14,
) -> dict:
    """
    Generate a 14-day cash flow forecast based on user parameters.
    """
    random.seed(42)
    today = date.today()
    balance = current_balance
    forecast_days = []

    # If no monthly_income provided, use a default fallback for demo
    fixed_income = monthly_income if monthly_income > 0 else 450_000.0
    # Distributed daily expense based on monthly total plus randomness
    daily_base_expense = (monthly_expenses / 30.0) if monthly_expenses > 0 else random.uniform(3_000, 12_000)

    for i in range(days):
        forecast_date = today + timedelta(days=i + 1)
        day_of_month = forecast_date.day
        weekday = forecast_date.weekday()

        # Income logic (Assume salary on 25th)
        income = 0.0
        if day_of_month == 25:
            income = fixed_income

        # Expense logic
        expense = daily_base_expense
        if weekday >= 5:  # weekend spike
            expense *= 1.5
        
        # Add some noise
        expense *= random.uniform(0.8, 1.2)

        balance = balance + income - expense
        confidence = max(0.60, 0.95 - (i * 0.025))

        forecast_days.append({
            "date": forecast_date.isoformat(),
            "predicted_balance": round(balance, 2),
            "predicted_income": round(income, 2),
            "predicted_expense": round(expense, 2),
            "confidence": round(confidence, 2),
        })

    min_balance = min(d["predicted_balance"] for d in forecast_days)
    safe_to_spend = max(0, round(current_balance - abs(min(0, min_balance)) - (monthly_expenses * 0.1), 2))

    risk_alert = None
    if min_balance < (monthly_expenses * 0.2):
        risk_alert = f"⚡️ Predicted low point of ₦{min_balance:,.2f} — watch your spending!"

    return {
        "forecast": forecast_days,
        "current_balance": current_balance,
        "safe_to_spend": safe_to_spend,
        "risk_alert": risk_alert,
    }

    return {
        "forecast": forecast_days,
        "current_balance": current_balance,
        "safe_to_spend": safe_to_spend,
        "risk_alert": risk_alert,
    }
